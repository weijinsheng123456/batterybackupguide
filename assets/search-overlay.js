(function () {
  "use strict";
  var INDEX_URL = "/assets/search-index.json";
  var MAX_RESULTS = 12;
  var index = [];
  var indexLoaded = false;
  var activeIndex = -1;
  var debounceTimer = null;
  var categoryLabels = {
    "buying-guide": "Buying Guide",
    comparison: "Comparison",
    survival: "Survival",
    "how-to": "How To",
    medical: "Medical",
    specialized: "Specialized",
    general: "General"
  };
  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }
  ready(function () {
    injectStyles();
    var trigger = document.createElement("button");
    trigger.type = "button";
    trigger.className = "bbg-search-trigger";
    trigger.setAttribute("aria-label", "Open search");
    trigger.innerHTML = "&#128269;";
    var overlay = document.createElement("div");
    overlay.className = "bbg-search-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-label", "Site search");
    overlay.innerHTML =
      '<div class="bbg-search-panel">' +
      '<button type="button" class="bbg-search-close" aria-label="Close search">&times;</button>' +
      '<div class="bbg-search-input-wrap">' +
      '<span aria-hidden="true">&#128269;</span>' +
      '<input class="bbg-search-input" type="search" placeholder="Search power stations, solar, CPAP, budget..." autocomplete="off">' +
      '</div>' +
      '<div class="bbg-search-meta">Type to search guides</div>' +
      '<div class="bbg-search-results" role="listbox" aria-label="Search results"></div>' +
      "</div>";
    document.body.appendChild(trigger);
    document.body.appendChild(overlay);
    var input = overlay.querySelector(".bbg-search-input");
    var resultsEl = overlay.querySelector(".bbg-search-results");
    var metaEl = overlay.querySelector(".bbg-search-meta");
    var closeBtn = overlay.querySelector(".bbg-search-close");
    trigger.addEventListener("click", openOverlay);
    closeBtn.addEventListener("click", closeOverlay);
    overlay.addEventListener("mousedown", function (event) {
      if (event.target === overlay) closeOverlay();
    });
    document.addEventListener("keydown", function (event) {
      var key = event.key.toLowerCase();
      if ((event.ctrlKey || event.metaKey) && key === "k") {
        event.preventDefault();
        openOverlay();
        return;
      }
      if (!overlay.classList.contains("is-open")) return;
      if (event.key === "Escape") closeOverlay();
      if (event.key === "ArrowDown") moveSelection(1, event);
      if (event.key === "ArrowUp") moveSelection(-1, event);
      if (event.key === "Enter") openSelected(event);
    });
    input.addEventListener("input", function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        runSearch(input.value.trim());
      }, 300);
    });
    resultsEl.addEventListener("mousemove", function (event) {
      var item = event.target.closest(".bbg-search-result");
      if (!item) return;
      setActive(Number(item.getAttribute("data-index")));
    });
    function openOverlay() {
      overlay.classList.add("is-open");
      document.documentElement.classList.add("bbg-search-lock");
      loadIndex();
      setTimeout(function () {
        input.focus();
        input.select();
      }, 40);
    }
    function closeOverlay() {
      overlay.classList.remove("is-open");
      document.documentElement.classList.remove("bbg-search-lock");
      activeIndex = -1;
    }
    function loadIndex() {
      if (indexLoaded) return;
      metaEl.textContent = "Loading guides...";
      fetch(INDEX_URL, { credentials: "same-origin" })
        .then(function (response) {
          if (!response.ok) throw new Error("Search index unavailable");
          return response.json();
        })
        .then(function (data) {
          index = Array.isArray(data) ? data : data.articles || [];
          indexLoaded = true;
          metaEl.textContent = input.value.trim() ? "" : index.length + " guides loaded";
          if (input.value.trim()) runSearch(input.value.trim());
        })
        .catch(function () {
          metaEl.textContent = "Search is temporarily unavailable";
        });
    }
    function runSearch(query) {
      activeIndex = -1;
      if (!query) {
        metaEl.textContent = indexLoaded ? index.length + " guides loaded" : "Type to search guides";
        resultsEl.innerHTML = "";
        return;
      }
      var results = search(query);
      metaEl.textContent = results.length + " result" + (results.length === 1 ? "" : "s") + " for \"" + query + "\"";
      render(results, query);
      if (results.length) setActive(0);
    }
    function search(query) {
      var tokens = tokenize(query);
      if (!tokens.length) return [];
      return index.map(function (item) {
        var title = normalize(item.title);
        var excerpt = normalize(item.excerpt || "");
        var category = normalize(item.category || "");
        var slug = normalize(item.slug || item.id || "");
        var haystack = title + " " + excerpt + " " + category + " " + slug;
        var score = 0;
        var allMatched = true;
        tokens.forEach(function (token) {
          if (haystack.indexOf(token) === -1) {
            allMatched = false;
            return;
          }
          if (title.indexOf(token) !== -1) score += 12;
          else if (excerpt.indexOf(token) !== -1) score += 4;
          else score += 1;
        });
        if (!score) return null;
        if (allMatched) score *= 2;
        return { item: item, score: score };
      }).filter(Boolean).sort(function (a, b) {
        return b.score - a.score;
      }).slice(0, MAX_RESULTS).map(function (entry) {
        return entry.item;
      });
    }
    function render(items, query) {
      if (!items.length) {
        resultsEl.innerHTML = '<div class="bbg-search-empty">No guides found. Try "solar", "budget", or "CPAP".</div>';
        return;
      }
      resultsEl.innerHTML = items.map(function (item, i) {
        var category = item.category || "general";
        var label = categoryLabels[category] || titleCase(category);
        return '<a class="bbg-search-result" role="option" data-index="' + i + '" href="' + escapeAttr(item.url || "#") + '">' +
          '<div class="bbg-search-result-head">' +
          '<span class="bbg-search-badge bbg-search-badge-' + escapeAttr(category) + '">' + escapeHtml(label) + "</span>" +
          '<strong>' + highlight(item.title || "Untitled", query) + "</strong>" +
          "</div>" +
          '<p>' + highlight(item.excerpt || "", query) + "</p>" +
          "</a>";
      }).join("");
    }
    function moveSelection(delta, event) {
      var items = getResults();
      if (!items.length) return;
      event.preventDefault();
      setActive((activeIndex + delta + items.length) % items.length);
    }
    function openSelected(event) {
      var items = getResults();
      if (activeIndex < 0 || !items[activeIndex]) return;
      event.preventDefault();
      window.location.href = items[activeIndex].href;
    }
    function setActive(index) {
      var items = getResults();
      activeIndex = index;
      items.forEach(function (item, i) {
        item.classList.toggle("is-active", i === activeIndex);
        item.setAttribute("aria-selected", i === activeIndex ? "true" : "false");
      });
      if (items[activeIndex]) items[activeIndex].scrollIntoView({ block: "nearest" });
    }

    function getResults() {
      return Array.prototype.slice.call(resultsEl.querySelectorAll(".bbg-search-result"));
    }
  });
  function normalize(text) {
    return String(text || "").toLowerCase().replace(/[^a-z0-9\s-]/g, " ").trim();
  }
  function tokenize(text) {
    return normalize(text).split(/\s+/).filter(Boolean);
  }
  function highlight(text, query) {
    var escaped = escapeHtml(text);
    tokenize(query).forEach(function (token) {
      var safe = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      escaped = escaped.replace(new RegExp("(" + safe + ")", "gi"), "<mark>$1</mark>");
    });
    return escaped;
  }
  function escapeHtml(text) {
    var div = document.createElement("div");
    div.textContent = String(text || "");
    return div.innerHTML;
  }
  function escapeAttr(text) {
    return escapeHtml(text).replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function titleCase(text) {
    return String(text || "general").replace(/-/g, " ").replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
  }
  function injectStyles() {
    if (document.getElementById("bbg-search-overlay-styles")) return;
    var style = document.createElement("style");
    style.id = "bbg-search-overlay-styles";
    style.textContent = ".bbg-search-lock{overflow:hidden}.bbg-search-trigger{position:fixed;right:22px;bottom:22px;z-index:9998;width:52px;height:52px;border:0;border-radius:50%;background:#2563eb;color:#fff;font-size:22px;box-shadow:0 14px 34px rgba(37,99,235,.34);cursor:pointer;transition:transform .2s,box-shadow .2s,background .2s}.bbg-search-trigger:hover{background:#1d4ed8;transform:translateY(-2px);box-shadow:0 18px 44px rgba(37,99,235,.42)}.bbg-search-overlay{position:fixed;inset:0;z-index:9999;display:flex;align-items:flex-start;justify-content:center;padding:9vh 20px 24px;background:rgba(8,13,24,.76);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);opacity:0;visibility:hidden;transition:opacity .22s ease,visibility .22s ease}.bbg-search-overlay.is-open{opacity:1;visibility:visible}.bbg-search-panel{position:relative;width:min(760px,100%);max-height:min(760px,84vh);display:flex;flex-direction:column;background:#fff;color:#111827;border:1px solid rgba(255,255,255,.18);border-radius:16px;box-shadow:0 30px 90px rgba(0,0,0,.35);font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;transform:translateY(12px) scale(.98);transition:transform .22s ease;overflow:hidden}.bbg-search-overlay.is-open .bbg-search-panel{transform:translateY(0) scale(1)}.bbg-search-close{position:absolute;top:12px;right:12px;width:34px;height:34px;border:0;border-radius:8px;background:#f3f4f6;color:#6b7280;font-size:24px;line-height:1;cursor:pointer;transition:background .2s,color .2s}.bbg-search-close:hover{background:#e5e7eb;color:#111827}.bbg-search-input-wrap{display:flex;align-items:center;gap:12px;padding:24px 58px 14px 24px;border-bottom:1px solid #eef2f7}.bbg-search-input-wrap span{font-size:20px;color:#2563eb}.bbg-search-input{width:100%;border:0;outline:0;background:transparent;color:#111827;font:600 1.15rem/1.4 Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.bbg-search-input::placeholder{color:#9ca3af;font-weight:500}.bbg-search-meta{padding:10px 24px;color:#6b7280;font-size:.88rem;border-bottom:1px solid #f3f4f6}.bbg-search-results{overflow:auto;padding:10px;scrollbar-width:thin}.bbg-search-result{display:block;padding:15px 14px;margin-bottom:8px;border:1px solid #eef2f7;border-radius:10px;background:#fff;text-decoration:none;color:inherit;transition:border-color .18s,box-shadow .18s,background .18s,transform .18s}.bbg-search-result:hover,.bbg-search-result.is-active{border-color:#2563eb;background:#f8fbff;box-shadow:0 8px 24px rgba(37,99,235,.1);transform:translateY(-1px)}.bbg-search-result-head{display:flex;align-items:center;gap:9px;margin-bottom:7px}.bbg-search-result strong{color:#111827;font-size:1rem;line-height:1.35}.bbg-search-result p{margin:0;color:#64748b;font-size:.92rem;line-height:1.55}.bbg-search-result mark{background:#fef08a;color:inherit;padding:0 2px;border-radius:2px}.bbg-search-badge{flex:0 0 auto;padding:3px 8px;border-radius:5px;font-size:.68rem;font-weight:800;line-height:1.2;text-transform:uppercase;letter-spacing:.03em}.bbg-search-badge-buying-guide{background:#dbeafe;color:#1d4ed8}.bbg-search-badge-comparison{background:#fce7f3;color:#be185d}.bbg-search-badge-survival{background:#fed7aa;color:#9a3412}.bbg-search-badge-how-to{background:#d1fae5;color:#065f46}.bbg-search-badge-medical{background:#e0e7ff;color:#3730a3}.bbg-search-badge-specialized{background:#f3e8ff;color:#6b21a8}.bbg-search-badge-general{background:#f3f4f6;color:#4b5563}.bbg-search-empty{padding:44px 16px;text-align:center;color:#6b7280;font-size:.95rem}@media(max-width:640px){.bbg-search-trigger{right:16px;bottom:16px;width:48px;height:48px}.bbg-search-overlay{align-items:stretch;padding:12px}.bbg-search-panel{max-height:calc(100vh - 24px);border-radius:14px}.bbg-search-input-wrap{padding:20px 52px 12px 16px}.bbg-search-input{font-size:1rem}.bbg-search-meta{padding:9px 16px}.bbg-search-results{padding:8px}.bbg-search-result{padding:13px 12px}.bbg-search-result-head{align-items:flex-start;flex-direction:column;gap:7px}.bbg-search-result strong{font-size:.95rem}.bbg-search-result p{font-size:.86rem}}";
    document.head.appendChild(style);
  }
})();
