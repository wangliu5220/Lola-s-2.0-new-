// Keep track of the last processed URL
let lastUrl = location.href;

// Observe DOM changes to handle dynamically loaded content
const observer = new MutationObserver(() => {
  if (location.href !== lastUrl) {
    lastUrl = location.href;
    tryInsertBox();
  }
  // Also try insert in case product description just appeared
  tryInsertBox();
});

observer.observe(document.body, { childList: true, subtree: true });

function tryInsertBox() {
  // Only run on product pages
  if (!location.pathname.includes("/ip/")) return;

  const target = document.querySelector('div[data-testid="add-to-cart-section"]');
  if (!target || document.getElementById("walmart-extension-box")) return;

  insertBox(target);
}

function insertBox(target) {
  const box = document.createElement("div");
  box.id = "walmart-extension-box";
  box.textContent = "✨ Lola's 2.0 Recommendations ✨";

  Object.assign(box.style, {
    backgroundColor: "#83b866",
    color: "white",
    padding: "8px",
    borderRadius: "6px",
    marginTop: "10px",
    fontSize: "14px",
  });

  target.prepend(box);
}
