// document.addEventListener("DOMContentLoaded", async () => {
//   const button = document.getElementById("getRecsBtn");
//   const result = document.getElementById("result");

//   button.addEventListener("click", async () => {
//     result.textContent = "Loading UPC...";

//     const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
//     chrome.tabs.sendMessage(tab.id, { action: "get_upc" }, (response) => {
//       if (chrome.runtime.lastError) {
//         result.textContent = "Error: Unable to connect to page.";
//         return;
//       }
//       if (!response || !response.upc) {
//         result.textContent = "No UPC found on this page.";
//         return;
//       }
//       result.textContent = `UPC: ${response.upc}`;
//     });
//   });
// });
