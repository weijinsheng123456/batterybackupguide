/**
 * batterybackupguide.com — Client-side search
 * Loads search-index.json and provides real-time filtering.
 */
(function () {
  "use strict";

  var index = [];
  var searchBox = document.getElementById("search-input");
  var resultsContainer = document.getElementById("search-results");
  var statusEl = document.getElementById("search-status");

  if (!searchBox) return;

  // ── Load index ────────────────────────────────────────
  var xhr = new XMLHttpRequest();
  xhr.open("GET", "/assets/search-index.json", true);
  xhr.onload = function () {
    if (xhr.status === 200) {
      try {
        index = JSON.parse(xhr.responseText);
        if (statusEl) statusEl.textContent = index.length + " guides loaded";
      } catch (e) {
        if (statusEl) statusEl.textContent = "Failed to load search index";
      }
    }
  };
  xhr.send();

  // ── Search logic ──────────────────────────────────────
  function normalize(text) {
    return text.toLowerCase().replace(/[^a-z0-9\s-]/g, "").trim();
  }

  function tokenize(text) {
    return normalize(text).split(/\s+/).filter(Boolean);
  }

  function search(query) {
    if (!query || query.length < 1) return [];
    var tokens = tokenize(query);
    if (tokens.length === 0) return [];

    var scored = [];

    for (var i = 0; i < index.length; i++) {
      var item = index[i];
      var titleNorm = normalize(item.title);
      var excerptNorm = normalize(item.excerpt || "");
      var catNorm = normalize(item.category || "");
      var slugNorm = normalize(item.slug || "");

      var text = titleNorm + " " + excerptNorm + " " + catNorm + " " + slugNorm;
      var score = 0;
      var matchAll = true;

      for (var t = 0; t < tokens.length; t++) {
        var token = tokens[t];
        if (text.indexOf(token) !== -1) {
          // Title matches worth MUCH more
          if (titleNorm.indexOf(token) !== -1) score += 10;
          else if (excerptNorm.indexOf(token) !== -1) score += 3;
          else score += 1;
        } else {
          matchAll = false;
        }
      }

      // Bonus for matching ALL tokens
      if (matchAll) score *= 2;

      if (score > 0) {
        scored.push({ item: item, score: score });
      }
    }

    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.slice(0, 12).map(function (s) { return s.item; });
  }

  // ── Render results ────────────────────────────────────
  function render(items, query) {
    if (!resultsContainer) return;

    if (items.length === 0) {
      if (query.length > 0) {
        resultsContainer.innerHTML =
          '<div class="search-empty"><p>No guides found for <strong>"' +
          escapeHtml(query) +
          '"</strong></p><p>Try different keywords like "solar", "budget", or "CPAP".</p></div>';
      } else {
        resultsContainer.innerHTML = "";
      }
      return;
    }

    var html = '<div class="search-count">' + items.length + " guide" +
      (items.length !== 1 ? "s" : "") + " found</div>";

    for (var i = 0; i < items.length; i++) {
      var item = items[i];
      var badgeClass = item.category || "general";
      var badgeLabel = item.category.replace("-", " ") || "Guide";

      html +=
        '<a href="' + escapeAttr(item.url) + '" class="search-result">' +
        '<div class="search-result-title">' +
        '<span class="search-badge search-badge-' + badgeClass + '">' +
        badgeLabel +
        "</span> " +
        highlight(escapeHtml(item.title), query) +
        "</div>" +
        '<div class="search-result-excerpt">' +
        highlight(escapeHtml(item.excerpt || ""), query) +
        "</div>" +
        "</a>";
    }

    resultsContainer.innerHTML = html;
  }

  // ── Helpers ───────────────────────────────────────────
  function escapeHtml(text) {
    var div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  function escapeAttr(text) {
    return text.replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  function highlight(text, query) {
    if (!query || query.length < 1) return text;
    var tokens = tokenize(query);
    for (var i = 0; i < tokens.length; i++) {
      var regex = new RegExp("(" + tokens[i].replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      text = text.replace(regex, "<mark>$1</mark>");
    }
    return text;
  }

  // ── Event handlers ────────────────────────────────────
  var debounceTimer;

  searchBox.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    var query = searchBox.value.trim();
    debounceTimer = setTimeout(function () {
      var results = search(query);
      render(results, query);
    }, 200);
  });

  // Handle query params on page load (?q=xxx)
  var params = new URLSearchParams(window.location.search);
  var q = params.get("q");
  if (q) {
    searchBox.value = q;
    var results = search(q);
    render(results, q);
  }
})();
