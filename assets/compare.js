(function () {
  "use strict";

  var DATA_URL = "/assets/compare-data.json";
  var allProducts = [];
  var selected = [];

  function ready(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fn);
    else fn();
  }

  ready(function () {
    fetch(DATA_URL, { credentials: "same-origin" })
      .then(function (r) { return r.json(); })
      .then(function (data) {
        allProducts = data;
        renderGrid();
      })
      .catch(function () {
        document.getElementById("compare-app").innerHTML =
          '<div class="compare-error">Failed to load product data. Please try again later.</div>';
      });
  });

  function renderGrid() {
    var app = document.getElementById("compare-app");
    if (!app) return;

    var html = '<div class="compare-grid">';
    allProducts.forEach(function (p) {
      var checked = selected.indexOf(p.id) !== -1 ? "checked" : "";
      html +=
        '<label class="compare-card' + (checked ? " is-selected" : "") + '">' +
        '<input type="checkbox" class="compare-checkbox" value="' + p.id + '" ' + checked + '>' +
        '<div class="compare-card-img-wrap">' +
        '<img src="' + p.image + '" alt="' + p.name + '" loading="lazy" width="200" height="133">' +
        '</div>' +
        '<div class="compare-card-body">' +
        '<div class="compare-brand">' + p.brand + '</div>' +
        '<div class="compare-name">' + p.name + '</div>' +
        '<div class="compare-specs-line">' + p.capacity_wh + 'Wh &middot; ' + p.output_w + 'W &middot; ' + p.weight_lbs + ' lbs</div>' +
        '<div class="compare-price">' + p.price_range + '</div>' +
        '</div>' +
        '</label>';
    });
    html += '</div>';

    html += '<div class="compare-table-wrap" id="compare-table-wrap"></div>';

    app.innerHTML = html;

    // Bind checkbox events
    app.querySelectorAll(".compare-checkbox").forEach(function (cb) {
      cb.addEventListener("change", function () {
        if (this.checked) {
          if (selected.indexOf(this.value) === -1) selected.push(this.value);
        } else {
          selected = selected.filter(function (id) { return id !== this.value; }.bind(this));
        }
        updateCards();
        renderTable();
      });
    });
  }

  function updateCards() {
    document.querySelectorAll(".compare-card").forEach(function (card) {
      var cb = card.querySelector(".compare-checkbox");
      card.classList.toggle("is-selected", cb.checked);
    });
  }

  function getProduct(id) {
    for (var i = 0; i < allProducts.length; i++) {
      if (allProducts[i].id === id) return allProducts[i];
    }
    return null;
  }

  function renderTable() {
    var wrap = document.getElementById("compare-table-wrap");
    if (!wrap) return;

    if (selected.length < 2) {
      wrap.innerHTML = '<div class="compare-hint">Select at least 2 products to compare</div>';
      return;
    }

    var products = selected.map(getProduct).filter(Boolean);

    var fields = [
      { key: "capacity_wh", label: "Capacity", fmt: function (v) { return v + " Wh"; } },
      { key: "output_w", label: "Output", fmt: function (v) { return v + " W"; } },
      { key: "weight_lbs", label: "Weight", fmt: function (v) { return v + " lbs"; } },
      { key: "chemistry", label: "Battery" },
      { key: "cycle_life", label: "Cycle Life" },
      { key: "warranty", label: "Warranty" },
      { key: "charging", label: "Charge Time" },
      { key: "solar_input_w", label: "Solar Input", fmt: function (v) { return v + " W"; } },
      { key: "price_range", label: "Price Range" },
      { key: "best_for", label: "Best For" }
    ];

    var html = '<table class="compare-table">';
    html += '<thead><tr><th>Specification</th>';
    products.forEach(function (p) {
      html += '<th><a href="' + p.url + '">' + p.name + '</a></th>';
    });
    html += '</tr></thead><tbody>';

    fields.forEach(function (field) {
      html += '<tr><td class="compare-label">' + field.label + '</td>';
      products.forEach(function (p) {
        var val = p[field.key];
        val = val === undefined || val === null ? "—" : (field.fmt ? field.fmt(val) : val);
        html += '<td>' + val + '</td>';
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    wrap.innerHTML = html;
  }
})();
