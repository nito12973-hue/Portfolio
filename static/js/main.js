(() => {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", (event) => {
      const targetId = anchor.getAttribute("href");
      if (targetId && targetId !== "#") {
        const target = document.querySelector(targetId);
        if (target) {
          event.preventDefault();
          target.scrollIntoView({ behavior: "smooth" });
        }
      }
    });
  });
})();
