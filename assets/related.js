(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    // Only run on article pages (posts/)
    var slug = window.location.pathname.replace("/posts/", "").replace(/\/$/, "").replace(".html", "");
    if (!slug || window.location.pathname.indexOf("/posts/") === -1) return;

    var main = document.querySelector("main") || document.querySelector("#article-content");
    if (!main) return;

    // Load data and render
    var productsData = null;
    var articleMap = null;
    var searchIndex = null;
    var loaded = 0;

    function checkDone() {
      loaded++;
      if (loaded < 3) return;
      renderAll();
    }

    fetch("/assets/compare-data.json", { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (d) { productsData = d; checkDone(); })
      .catch(function () { checkDone(); });

    fetch("/assets/article-products.json", { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (d) { articleMap = d; checkDone(); })
      .catch(function () { checkDone(); });

    fetch("/assets/search-index.json", { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (d) { searchIndex = Array.isArray(d) ? d : d.articles || []; checkDone(); })
      .catch(function () { checkDone(); });

    function renderAll() {
      var html = "";
      // Section 1: Related Products
      html += renderRelatedProducts();
      // Section 2: Related Articles
      html += renderRelatedArticles();
      if (html) {
        var wrap = document.createElement("div");
        wrap.innerHTML = html;
        main.appendChild(wrap);
      }
    }

    function renderRelatedProducts() {
      if (!productsData || !articleMap) return "";
      var productIds = articleMap[slug];
      if (!productIds || !productIds.length) return "";

      var products = [];
      productIds.forEach(function (id) {
        for (var i = 0; i < productsData.length; i++) {
          if (productsData[i].id === id) {
            products.push(productsData[i]);
            break;
          }
        }
      });
      if (!products.length) return "";

      var h = '<div class="related-section" style="margin-top:40px;padding-top:32px;border-top:1px solid #e8e4dc">';
      h += '<h2 style="font-size:1.25rem;margin-bottom:20px">&#x1f4a1; Products Mentioned in This Guide</h2>';
      h += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px">';
      products.forEach(function (p) {
        h += '<a href="' + p.url + '" style="display:block;background:#fff;border:1px solid #eee;border-radius:10px;padding:12px;text-decoration:none;color:inherit;transition:border-color .2s,box-shadow .2s" onmouseover="this.style.borderColor=\'#2563eb\';this.style.boxShadow=\'0 2px 12px rgba(37,99,235,0.08)\'" onmouseout="this.style.borderColor=\'#eee\';this.style.boxShadow=\'none\'">';
        h += '<div style="aspect-ratio:3/2;overflow:hidden;border-radius:6px;background:#f8f8f8;margin-bottom:8px">';
        h += '<img src="' + p.image + '" alt="' + p.name + '" style="width:100%;height:100%;object-fit:cover" loading="lazy">';
        h += '</div>';
        h += '<div style="font-size:0.68rem;color:#888;text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px">' + p.brand + '</div>';
        h += '<div style="font-weight:700;font-size:0.82rem;color:#1a1a1a;line-height:1.3">' + p.name + '</div>';
        h += '<div style="font-size:0.75rem;color:#666;margin-top:3px">' + p.capacity_wh + 'Wh &middot; ' + p.output_w + 'W</div>';
        h += '<div style="font-size:0.78rem;color:#2563eb;font-weight:600;margin-top:4px">' + p.price_range + '</div>';
        h += '</a>';
      });
      h += '</div></div>';
      return h;
    }

    function renderRelatedArticles() {
      if (!searchIndex) return "";

      var current = null;
      for (var i = 0; i < searchIndex.length; i++) {
        if (searchIndex[i].slug === slug || searchIndex[i].id === slug) {
          current = searchIndex[i];
          break;
        }
      }
      if (!current) return "";

      var cat = current.category || "";
      var related = [];
      for (var i = 0; i < searchIndex.length; i++) {
        var a = searchIndex[i];
        if (a.slug === slug || a.id === slug) continue;
        if (a.category === cat && related.length < 3) {
          related.push(a);
        }
      }

      // If less than 3 in same category, add from other categories
      if (related.length < 3) {
        for (var i = 0; i < searchIndex.length && related.length < 3; i++) {
          var a = searchIndex[i];
          if (a.slug === slug || a.id === slug) continue;
          if (a.category !== cat) related.push(a);
        }
      }

      if (!related.length) return "";

      var h = '<div class="related-section" style="margin-top:32px;padding-top:32px;border-top:1px solid #e8e4dc">';
      h += '<h2 style="font-size:1.25rem;margin-bottom:20px">&#x1f4d6; You Might Also Like</h2>';
      h += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px">';
      related.forEach(function (a) {
        var badgeClass = a.category || "general";
        var badgeLabel = (a.category || "general").replace(/-/g, " ");
        h += '<a href="' + (a.url || "/posts/" + (a.slug || a.id)) + '" style="display:block;background:#fff;border:1px solid #eee;border-radius:10px;padding:14px;text-decoration:none;color:inherit;transition:border-color .2s,box-shadow .2s" onmouseover="this.style.borderColor=\'#2563eb\';this.style.boxShadow=\'0 2px 12px rgba(37,99,235,0.08)\'" onmouseout="this.style.borderColor=\'#eee\';this.style.boxShadow=\'none\'">';
        h += '<span style="display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.68rem;font-weight:700;text-transform:uppercase;margin-bottom:6px;background:#dbeafe;color:#1d4ed8">' + badgeLabel + '</span>';
        h += '<div style="font-weight:600;font-size:0.92rem;color:#1a1a1a;line-height:1.35">' + a.title + '</div>';
        h += '<div style="font-size:0.82rem;color:#666;margin-top:4px;line-height:1.4;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">' + (a.excerpt || "") + '</div>';
        h += '</a>';
      });
      h += '</div></div>';
      return h;
    }
  });
})();
