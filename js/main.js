/* TrackingMe.ca — shared site behaviour */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    initHeaderScroll();
    initMobileNav();
    initDropdowns();
    initFaqAccordions();
    initTabs();
    initRevealOnScroll();
    initForms();
    setYear();
  });

  function initHeaderScroll() {
    var header = document.getElementById("siteHeader");
    if (!header) return;
    var onScroll = function () {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initMobileNav() {
    var toggle = document.getElementById("navToggle");
    var nav = document.getElementById("mainNav");
    var scrim = document.getElementById("navScrim");
    if (!toggle || !nav) return;
    function close() {
      nav.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      if (scrim) scrim.classList.remove("is-open");
    }
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      if (scrim) scrim.classList.toggle("is-open", open);
    });
    if (scrim) scrim.addEventListener("click", close);
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () {
        if (window.innerWidth <= 960) close();
      });
    });
  }

  function initDropdowns() {
    var items = document.querySelectorAll(".main-nav li.has-dropdown");
    items.forEach(function (li) {
      var btn = li.querySelector(".nav-top-link");
      if (!btn) return;
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var isOpen = li.classList.contains("is-open");
        items.forEach(function (other) { other.classList.remove("is-open"); });
        if (!isOpen) li.classList.add("is-open");
      });
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".main-nav li.has-dropdown")) {
        items.forEach(function (li) { li.classList.remove("is-open"); });
      }
    });
  }

  function initFaqAccordions() {
    document.querySelectorAll(".faq-item").forEach(function (item) {
      var q = item.querySelector(".faq-q");
      if (!q) return;
      q.addEventListener("click", function () {
        var isOpen = item.classList.contains("is-open");
        var group = item.closest(".faq-list");
        if (group) {
          group.querySelectorAll(".faq-item").forEach(function (i) { i.classList.remove("is-open"); });
        }
        if (!isOpen) item.classList.add("is-open");
      });
    });
  }

  function initTabs() {
    document.querySelectorAll("[data-tabs]").forEach(function (wrap) {
      var buttons = wrap.querySelectorAll("[data-tab-btn]");
      var panels = wrap.querySelectorAll("[data-tab-panel]");
      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var target = btn.getAttribute("data-tab-btn");
          buttons.forEach(function (b) { b.classList.remove("is-active"); });
          panels.forEach(function (p) { p.classList.remove("is-active"); });
          btn.classList.add("is-active");
          var panel = wrap.querySelector('[data-tab-panel="' + target + '"]');
          if (panel) panel.classList.add("is-active");
        });
      });
    });
  }

  function initRevealOnScroll() {
    var els = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window) || !els.length) {
      els.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.01, rootMargin: "0px 0px -5% 0px" });
    els.forEach(function (el) { obs.observe(el); });
    // Safety net: guarantee content is visible even if an observer callback is missed.
    window.setTimeout(function () {
      els.forEach(function (el) { el.classList.add("is-visible"); });
    }, 4000);
  }

  function captureUtm() {
    var params = new URLSearchParams(window.location.search);
    return {
      utm_source: params.get("utm_source") || "",
      utm_medium: params.get("utm_medium") || "",
      utm_campaign: params.get("utm_campaign") || "",
      utm_term: params.get("utm_term") || "",
    };
  }

  function submitLead(form) {
    var endpoint = window.LEAD_ENDPOINT;
    var data = {};
    new FormData(form).forEach(function (value, key) {
      if (key === "_gotcha") return;
      if (data[key] !== undefined) {
        data[key] = Array.isArray(data[key]) ? data[key].concat(value) : [data[key], value];
      } else {
        data[key] = value;
      }
    });
    data.form = form.getAttribute("data-lead-form") || "unknown";
    data.landing_page = window.location.pathname;
    data.timestamp = new Date().toISOString();
    Object.assign(data, captureUtm());

    if (!endpoint || endpoint.indexOf("REPLACE_WITH") === 0) {
      // Apps Script Web App URL not configured yet (see js/lead-config.js) —
      // log instead of silently discarding the submission.
      console.warn("Lead capture endpoint not configured — submission not sent:", data);
      return Promise.resolve();
    }

    // Apps Script Web Apps don't return CORS headers to cross-origin reads,
    // so the response body can't be inspected here — mode:'no-cors' still
    // delivers the request, we just treat "no network error" as success.
    return fetch(endpoint, {
      method: "POST",
      mode: "no-cors",
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(data),
    });
  }

  function initForms() {
    document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        var honeypot = form.querySelector('[name="_gotcha"]');
        if (honeypot && honeypot.value) return; // bot — drop silently, no UX change

        var submitBtn = form.querySelector('[type="submit"]');
        if (submitBtn) submitBtn.disabled = true;

        submitLead(form).finally(function () {
          var successEl = form.parentElement.querySelector(".form-success");
          form.style.display = "none";
          if (successEl) successEl.classList.add("is-visible");
          successEl && successEl.scrollIntoView({ behavior: "smooth", block: "center" });
        });
      });
    });
  }

  function setYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }
})();
