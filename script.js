(function () {
  if (window.location.protocol !== "file:" && /\/index\.html$/.test(window.location.pathname)) {
    window.location.replace(window.location.pathname.replace(/index\.html$/, "") + window.location.search + window.location.hash);
    return;
  }

  const header = document.querySelector("[data-header]");
  const navToggle = document.querySelector("[data-nav-toggle]");
  const navMenu = document.querySelector("[data-nav-menu]");

  function setHeaderState() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  setHeaderState();
  window.addEventListener("scroll", setHeaderState, { passive: true });

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
      navMenu.classList.toggle("is-open", !expanded);
    });

    navMenu.addEventListener("click", (event) => {
      if (event.target instanceof HTMLAnchorElement) {
        navToggle.setAttribute("aria-expanded", "false");
        navMenu.classList.remove("is-open");
      }
    });
  }

  document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = String(new Date().getFullYear());
  });

  const textWalker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  let textNode;
  while ((textNode = textWalker.nextNode())) textNodes.push(textNode);
  textNodes.forEach((node) => {
    node.nodeValue = node.nodeValue
      .replace(/Request availability/g, "Contact details")
      .replace(/requesting availability/g, "contacting us")
      .replace(/contact@shinetimecleanersllc\.com/g, "Email unavailable");
  });

  document.querySelectorAll("[data-accordion]").forEach((accordion) => {
    accordion.addEventListener("click", (event) => {
      const button = event.target.closest("button");
      if (!button || !accordion.contains(button)) return;
      const item = button.closest(".accordion-item");
      const isOpen = item.classList.contains("is-open");
      item.classList.toggle("is-open", !isOpen);
      button.setAttribute("aria-expanded", String(!isOpen));
    });
  });

}());
