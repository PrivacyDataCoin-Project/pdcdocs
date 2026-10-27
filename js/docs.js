(function () {
  document.documentElement.setAttribute("data-theme", "brand");

  var input = document.querySelector(".search");
  var links = Array.prototype.slice.call(document.querySelectorAll(".nav-group a"));
  if (input) {
    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      links.forEach(function (link) {
        var group = link.parentElement;
        var show = !q || link.textContent.toLowerCase().indexOf(q) !== -1;
        link.hidden = !show;
        if (group) group.hidden = !group.querySelector("a:not([hidden])");
      });
    });
  }

  var side = document.querySelector(".sidebar");
  var backdrop = document.querySelector("[data-backdrop]");
  var docsMenus = Array.prototype.slice.call(
    document.querySelectorAll("[data-docs-menu], [data-docs-menu-mobile]")
  );
  var menuBtn = document.querySelector("[data-menu]");
  var mobilePanel = document.querySelector("[data-mobile]");

  function setSideOpen(open) {
    if (!side) return;
    side.classList.toggle("open", open);
    if (backdrop) backdrop.hidden = !open;
    docsMenus.forEach(function (btn) {
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  function setMobileOpen(open) {
    if (!mobilePanel) return;
    mobilePanel.classList.toggle("open", open);
    if (menuBtn) menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
  }

  docsMenus.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setMobileOpen(false);
      setSideOpen(!side.classList.contains("open"));
    });
  });

  if (menuBtn && mobilePanel) {
    menuBtn.addEventListener("click", function () {
      setSideOpen(false);
      setMobileOpen(!mobilePanel.classList.contains("open"));
    });
  }

  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setSideOpen(false);
      setMobileOpen(false);
    });
  }

  document.querySelectorAll(".sidebar a").forEach(function (link) {
    link.addEventListener("click", function () { setSideOpen(false); });
  });

  if ("scrollRestoration" in history) {
    history.scrollRestoration = "manual";
  }

  function navOffset() {
    var nav = document.querySelector(".site-nav");
    return (nav ? nav.getBoundingClientRect().height : 72) + 12;
  }

  function scrollToHeading(id, smooth) {
    if (!id) return false;
    var el = document.getElementById(id);
    if (!el) return false;
    var top = el.getBoundingClientRect().top + window.pageYOffset - navOffset();
    window.scrollTo({ top: Math.max(0, top), behavior: smooth ? "smooth" : "auto" });
    return true;
  }

  document.querySelectorAll('.toc a[href^="#"], article a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      var href = link.getAttribute("href") || "";
      var id = decodeURIComponent(href.slice(1));
      if (!id || !document.getElementById(id)) return;
      event.preventDefault();
      if (history.pushState) history.pushState(null, "", "#" + id);
      else location.hash = id;
      scrollToHeading(id, true);
    });
  });

  function syncHash() {
    var id = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    if (id) scrollToHeading(id, false);
  }

  window.addEventListener("hashchange", syncHash);
  window.addEventListener("pageshow", syncHash);
  window.addEventListener("load", function () {
    syncHash();
    setTimeout(syncHash, 0);
    setTimeout(syncHash, 100);
  });
  syncHash();
})();
