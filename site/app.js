/* CleanYourRoku: tabs, carousel arrows, the rail menu and pop-ups. No libraries, no tracking. */
(function () {
  var tabs = Array.prototype.slice.call(document.querySelectorAll(".tab"));

  // Only the home page has tabs
  function initTabs() {
    var panels = tabs.map(function (t) { return document.getElementById(t.getAttribute("aria-controls")); });
    var arrows = document.querySelector(".arrows");
    var prev = document.getElementById("prev");
    var next = document.getElementById("next");
    var current = 0;

    function scroller() { return panels[current].querySelector(".cards"); }

    function updateArrows() {
      var s = scroller();
      arrows.hidden = s.scrollWidth <= s.clientWidth + 1;
      prev.disabled = s.scrollLeft <= 1;
      next.disabled = s.scrollLeft + s.clientWidth >= s.scrollWidth - 1;
    }

    function show(i, focus) {
      current = i;
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        panels[n].hidden = !on;
      });
      scroller().scrollLeft = 0;
      updateArrows();
      if (focus) tabs[i].focus();
    }

    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () {
        show(i);
        history.replaceState(null, "", "#" + t.textContent.trim().toLowerCase().replace(/\s+/g, "-"));
      });
      t.addEventListener("keydown", function (e) {
        var n = tabs.length;
        var to = { ArrowRight: (i + 1) % n, ArrowLeft: (i - 1 + n) % n, Home: 0, End: n - 1 }[e.key];
        if (to === undefined) return;
        e.preventDefault();
        show(to, true);
      });
    });

    panels.forEach(function (p) { p.querySelector(".cards").addEventListener("scroll", updateArrows, { passive: true }); });
    window.addEventListener("resize", updateArrows);

    function page(dir) {
      var s = scroller();
      var card = s.querySelector(".card");
      var gap = parseFloat(getComputedStyle(s).columnGap) || 0;
      s.scrollBy({ left: dir * (card.offsetWidth + gap), behavior: "smooth" });
    }
    prev.addEventListener("click", function () { page(-1); });
    next.addEventListener("click", function () { page(1); });

    // Opens the tab named in the address, like cleanyourroku.com/#faq
    var start = tabs.findIndex(function (t) { return "#" + t.textContent.trim().toLowerCase().replace(/\s+/g, "-") === location.hash; });
    show(start < 0 ? 0 : start);
  }
  if (tabs.length) initTabs();

  // Rail menu
  var menuBtn = document.getElementById("menu-btn");
  var menu = document.getElementById("menu");

  function closeMenu() {
    menu.hidden = true;
    menuBtn.setAttribute("aria-expanded", "false");
  }

  menuBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = menu.hidden;
    menu.hidden = !open;
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) menu.querySelector("a, button").focus();
  });
  document.addEventListener("click", function (e) { if (!menu.contains(e.target)) closeMenu(); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !menu.hidden) {
      closeMenu();
      menuBtn.focus();
    }
  });

  // The Photos pop-up lines up with the hero banner, which sits off-center beside the rail
  var hero = document.querySelector(".hero");
  var wide = document.querySelector(".sheet-wide");

  function alignWide() {
    if (!wide || !wide.open) return;
    var r = hero.getBoundingClientRect();
    wide.style.left = r.left + "px";
    wide.style.width = r.width + "px";
  }
  window.addEventListener("resize", alignWide);

  function openSheet(d) {
    d.showModal();
    alignWide();
  }

  // Pop-ups open over the current tab and leave it as it was.
  // The browser returns focus to whatever had it at showModal(), however the pop-up is closed.
  Array.prototype.forEach.call(document.querySelectorAll("[data-sheet]"), function (b) {
    b.addEventListener("click", function () {
      var opener = menu.contains(b) ? menuBtn : b;
      closeMenu();
      opener.focus();
      openSheet(document.getElementById(b.dataset.sheet));
    });
  });
  Array.prototype.forEach.call(document.querySelectorAll(".sheet"), function (d) {
    d.querySelector(".sheet-close").addEventListener("click", function () { d.close(); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
  });

  // Links from the Privacy, Terms and Support menus, like index.html#contact
  var linked = location.hash && document.getElementById(location.hash.slice(1));
  if (linked && linked.showModal) openSheet(linked);
})();
