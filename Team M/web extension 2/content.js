// Only run on product pages (optional)
if (window.location.pathname.includes("/ip/")) {
  const observer = new MutationObserver(() => {
    const target = document.querySelector("#ip-prod-desc-atf-div-1");

    if (target && !document.getElementById("walmart-extension-box")) {
      insertBox(target);
      observer.disconnect(); // stop watching once inserted
    }
  });

  observer.observe(document.body, { childList: true, subtree: true });
}

function insertBox(target) {
  const box = document.createElement("div");
  box.id = "walmart-extension-box";
  box.textContent = "✨ Recommendations: ... ✨";

  Object.assign(box.style, {
    backgroundColor: "#1f984df6",
    color: "white",
    padding: "8px",
    borderRadius: "6px",
    marginTop: "10px",
    fontSize: "14px",
  });

  target.prepend(box);
}
