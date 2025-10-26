chrome.runtime.onMessage.addListener((req, sender, sendResponse) => {
  if (req.action === "get_upc") {
    try {
      const script = document.querySelector('script#__NEXT_DATA__');
      if (!script) {
        sendResponse({ upc: null });
        return;
      }
      const json = JSON.parse(script.textContent);
      const upc = json?.props?.pageProps?.initialData?.data?.product?.upc || null;
      sendResponse({ upc });
    } catch (err) {
      console.error("Failed to extract UPC:", err);
      sendResponse({ upc: null });
    }
  }
});
