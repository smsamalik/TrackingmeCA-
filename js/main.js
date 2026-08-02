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

  function initForms() {
    document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        var successEl = form.parentElement.querySelector(".form-success");
        form.style.display = "none";
        if (successEl) successEl.classList.add("is-visible");
        successEl && successEl.scrollIntoView({ behavior: "smooth", block: "center" });
        // NOTE: This is a front-end placeholder. Wire this submit handler to
        // your CRM/lead-routing endpoint (e.g. HubSpot, Salesforce, or a
        // serverless form handler) before go-live.
      });
    });
  }

  function setYear() {
    document.querySelectorAll("[data-year]").forEach(function (el) {
      el.textContent = new Date().getFullYear();
    });
  }
})();
