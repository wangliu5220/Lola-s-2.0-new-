document.addEventListener("DOMContentLoaded", async () => {
  const button = document.getElementById("getRecsBtn");
  const result = document.getElementById("result");

  // Helper: Extract product (same logic as working Walmart script)
  function extractProductFromPage() {
    try {
      // ld+json approach
      const ldJson = [...document.querySelectorAll('script[type="application/ld+json"]')]
        .map(s => {
          try { return JSON.parse(s.textContent); } catch { return null; }
        })
        .find(obj => obj && (obj.gtin13 || obj.sku || obj.name || obj.description));

      if (ldJson) {
        return {
          upc: ldJson.gtin13 ?? ldJson.sku ?? null,
          name: ldJson.name ?? null,
          description: ldJson.description ?? null,
        };
      }

      // __NEXT_DATA__ fallback
      const nextData = document.querySelector("script#__NEXT_DATA__");
      if (nextData) {
        const json = JSON.parse(nextData.textContent);
        const p = json?.props?.pageProps?.initialData?.data?.product ?? {};
        return {
          upc: p.upc ?? null,
          name: p.name ?? null,
          description: p.description ?? null,
        };
      }

      return null;
    } catch (err) {
      console.error("❌ extractProductFromPage failed:", err);
      return null;
    }
  }

  // Button handler
  button.addEventListener("click", async () => {
    result.textContent = "Loading UPC...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: extractProductFromPage, // <-- use same working logic
      },
      async (injectionResults) => {
        if (chrome.runtime.lastError) {
          result.textContent = "❌ Unable to access page.";
          console.error(chrome.runtime.lastError.message);
          return;
        }

        const product = injectionResults?.[0]?.result;

        if (!product || (!product.upc && !product.name && !product.description)) {
          result.textContent = "No product info found on this page.";
          return;
        }

        result.textContent =
          `UPC: ${product.upc || "N/A"}\nName: ${product.name || "N/A"}\nDescription: ${product.description || "N/A"}`;

        await getRecommendation(product);
      }
    );
  });

  // Fetch recommendation from FastAPI
  async function getRecommendation(product) {
    try {
      result.textContent = "Fetching recommendations...";

      const req = {
        name: product.name ?? null,
        description: product.description ?? null,
      };

      const response = await fetch("http://127.0.0.1:8000/qdrant", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(req),
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      let data = await response.json();
      data = data.best_match; // backend shape

      // Normalize fields so UI never breaks
      const nf = data?.Nutrition_facts ?? {};

      const normalized = {
        product_name: data?.product_name ?? "N/A",
        snap_eligible: data?.snap_eligible ?? false,
        price: typeof data?.price === "number" ? data.price : null,
        universal_product_code: data?.universal_product_code || product.upc || null,
        product_URL: data?.product_URL || "#",
        avg_rating: data?.avg_rating ?? "N/A",
        image_url: data?.image_url || "",

        Nutrition_facts: {
          calories: nf.calories ?? "N/A",
          total_fat_absolute: nf.total_fat_absolute ?? "N/A",
          total_fat_DV: nf.total_fat_DV ?? "N/A",
          sodium_absolute: nf.sodium_absolute ?? "N/A",
          sodium_DV: nf.sodium_DV ?? "N/A",
          total_carbs_absolute: nf.total_carbs_absolute ?? "N/A",
          total_carbs_DV: nf.total_carbs_DV ?? "N/A",
          total_sugars_absolute: nf.total_sugars_absolute ?? "N/A",
          protein_absolute: nf.protein_absolute ?? "N/A",
          ingredients: nf.ingredients ?? [],
          ultraprocessed: nf.ultraprocessed ?? false,
          category: nf.category ?? "",
        },
      };

      displayRecommendation(normalized);
    } catch (err) {
      console.error("❌ getRecommendation failed:", err);
      result.textContent = "❌ Failed to load recommendations.";
    }
  }

  // Render recommendation inside popup
  function displayRecommendation(data) {
    const facts = data.Nutrition_facts;
    const snapEligible = data.snap_eligible ? "✅ SNAP Eligible" : "❌ Not SNAP Eligible";
    const processedTag = facts.ultraprocessed ? "⚠️ Ultraprocessed" : "🌿 Minimally Processed";

    result.innerHTML = `
      <div class="product-card">
        <a href="${data.product_URL}" target="_blank">
          <img src="${data.image_url}" alt="${data.product_name}" class="product-img" />
        </a>

        <div class="product-name">${data.product_name}</div>
        <div class="product-meta">
          $${(data.price ?? 0).toFixed(2)} • ⭐ ${data.avg_rating}
        </div>

        <div>
          <span class="tag snap">${snapEligible}</span>
          <span class="tag processed">${processedTag}</span>
        </div>

        <div class="nutrition-section">
          <h3>Nutrition Facts</h3>
          <ul class="nutrition-list">
            <li><span>Calories</span><span>${facts.calories}</span></li>
            <li><span>Total Fat</span><span>${facts.total_fat_absolute} (${facts.total_fat_DV})</span></li>
            <li><span>Sodium</span><span>${facts.sodium_absolute} (${facts.sodium_DV})</span></li>
            <li><span>Total Carbs</span><span>${facts.total_carbs_absolute} (${facts.total_carbs_DV})</span></li>
            <li><span>Total Sugars</span><span>${facts.total_sugars_absolute}</span></li>
            <li><span>Protein</span><span>${facts.protein_absolute}</span></li>
          </ul>
          <div class="ingredients">
            <strong>Ingredients:</strong> ${facts.ingredients.join(", ")}
          </div>
        </div>
      </div>
    `;
  }
});
