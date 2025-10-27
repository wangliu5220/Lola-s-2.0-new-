document.getElementById("insertBox").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    function: insertBox
  });
});

function insertBox() {
  const existingBox = document.getElementById("walmart-extension-box");
  if (existingBox) return; // prevent duplicates

  // Try to find the product description element
  const target = document.querySelector("#ip-prod-desc-atf-div-1");
  if (!target) {
    alert("Couldn't find the product description section on this page.");
    return;
  }

  // Create the box
  const box = document.createElement("div");
  box.id = "walmart-extension-box";
  box.textContent = "✨ Inserted by your Chrome Extension ✨";

  // Style the box (inline element inside the description)
  Object.assign(box.style, {
    backgroundColor: "#1f984df6",
    color: "white",
    padding: "8px",
    borderRadius: "6px",
    marginTop: "10px",
    fontSize: "14px",
  });

  // Append the box inside the product description area
  target.prepend(box);
}
