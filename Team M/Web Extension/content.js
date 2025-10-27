function extractUPC() {
  try {
    const script = document.querySelector('script#__NEXT_DATA__');
    if (!script) return null;

    const json = JSON.parse(script.textContent);
    const upc = json?.props?.pageProps?.initialData?.data?.product?.upc || null;

    if (upc) {
      console.log(" Walmart UPC:", upc);
      chrome.runtime.sendMessage({ action: "upc_found", upc });
      return upc;
    }

    return null;
  } catch (err) {
    console.error("Failed to extract UPC:", err);
    return null;
  }
}

// Run once when the content script loads
function initUPCWatcher() {
  let lastUrl = location.href;
  let lastUPC = null;

  const checkUPC = () => {
    const upc = extractUPC();
    if (upc && upc !== lastUPC) {
      lastUPC = upc;
    }
  };

  window.addEventListener("load", checkUPC);

  const observer = new MutationObserver(() => {
    if (location.href !== lastUrl) {
      lastUrl = location.href;
      console.log("🔄 Walmart URL changed:", lastUrl);
      // setTimeout(checkUPC, 800); // delay a bit to let new data load
      tryInsertBox();
      checkUPC();
    }
    // Also try insert in case product description just appeared
    tryInsertBox();
  });

  observer.observe(document, { subtree: true, childList: true });
}

initUPCWatcher();

function tryInsertBox() {
  console.log("hi");
  // Only run on product pages
  if (!location.pathname.includes("/ip/")) return;

  const target = document.querySelector("#main-title");
  if (!target || document.getElementById("walmart-extension-box")){
    console.log("not found");
    return;
  } 

  insertBox(target);
}

function insertBox(target) {
  console.log("insert");
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
