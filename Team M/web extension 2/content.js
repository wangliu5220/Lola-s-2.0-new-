function insertRecommendationBox(upc) {
  // Prevent duplicates
  if (document.getElementById("recommendation-box")) return;

  // Walmart’s React layout is dynamic — wait until the product description is available
  const checkInterval = setInterval(() => {
    const descriptionSection =
      document.querySelector('[data-testid="about-section"]') ||
      document.querySelector('[data-testid="product-description"]') ||
      document.querySelector('section[data-item="description"]') ||
      document.querySelector("section[data-testid='product-description']");

    if (descriptionSection) {
      clearInterval(checkInterval);

      // Create the embedded box
      const box = document.createElement("div");
      box.id = "recommendation-box";
      box.innerHTML = `
        <div style="
          background: #f4f9ff;
          border-left: 4px solid #0071ce;
          padding: 16px;
          margin-bottom: 24px;
          border-radius: 4px;
        ">
          <h3 style="margin: 0 0 8px 0; font-size: 18px; color: #0071ce;">
            Recommendation
          </h3>
          <p style="margin: 0; font-size: 15px; color: #111;">
            ${upc ? `Product UPC: <strong>${upc}</strong>` : "No UPC found for this product."}
          </p>
        </div>
      `;

      // Embed box directly *before* the description section
      descriptionSection.parentNode.insertBefore(box, descriptionSection);
      console.log("✅ Embedded Recommendation box added inside Walmart layout");
    }
  }, 1000); // check every 1s until the section loads
}
