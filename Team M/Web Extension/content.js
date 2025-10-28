function extractUPC() {
  try {
    // 1️⃣ Try to extract from live DOM (React-injected ld+json)
    const ldJson = [...document.querySelectorAll('script[type="application/ld+json"]')]
      .map(s => {
        try { return JSON.parse(s.textContent); } catch { return null; }
      })
      .find(obj => obj && (obj.gtin13 || obj.sku));
    const upc = ldJson?.gtin13 || ldJson?.sku;

    if (upc) {
      console.log("📦 Walmart UPC (ld+json):", upc);
      chrome.runtime.sendMessage({ action: "upc_found", upc });
      return upc;
    }

    // 2️⃣ Fall back to __NEXT_DATA__ (first load only)
    const script = document.querySelector('script#__NEXT_DATA__');
    if (script) {
      const json = JSON.parse(script.textContent);
      const upc2 = json?.props?.pageProps?.initialData?.data?.product?.upc || null;
      if (upc2) {
        console.log("📦 Walmart UPC (NEXT_DATA):", upc2);
        chrome.runtime.sendMessage({ action: "upc_found", upc: upc2 });
        return upc2;
      }
    }

    return null;
  } catch (err) {
    console.error("Failed to extract UPC:", err);
    return null;
  }
}

function insertBox(target) {
  const existing = document.getElementById("walmart-extension-box");
  if (existing) return;

  const box = document.createElement("div");
  box.id = "walmart-extension-box";
  box.textContent = "Lola's 2.0 Recommendations";

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

function tryInsertBox() {
  const target = document.querySelector('div[data-testid="add-to-cart-section"]');
  if (target) insertBox(target);
}

function initUPCWatcher() {
  console.log("👀 Starting Walmart UPC watcher...");

  // Run on initial load
  extractUPC();
  tryInsertBox();

  // ✅ Hook into Next.js router events (no full reload)
  const router = window.next?.router;
  if (router) {
    router.events.on("routeChangeComplete", (url) => {
      console.log("🔄 Walmart route changed:", url);
      setTimeout(() => {
        extractUPC();
        tryInsertBox();
      }, 1200); // give React time to re-render content
    });
  } else {
    console.warn("⚠️ Next.js router not found — fallback to MutationObserver.");
    // fallback: monitor URL and DOM
    let lastUrl = location.href;
    const observer = new MutationObserver(() => {
      const currentUrl = location.href;
      if (currentUrl !== lastUrl) {
        lastUrl = currentUrl;
        console.log("🔄 Walmart URL changed (fallback):", currentUrl);
        setTimeout(() => {
          extractUPC();
          tryInsertBox();
        }, 1200);
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
}

initUPCWatcher();
