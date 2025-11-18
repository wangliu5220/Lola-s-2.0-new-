document.addEventListener("DOMContentLoaded", async () => {
  const button = document.getElementById("getRecsBtn");
  const result = document.getElementById("result");

  button.addEventListener("click", async () => {
    result.textContent = "Loading UPC...";

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: () => {
          try {
            // 1️⃣ Extract UPC from ld+json
            const ldJson = [...document.querySelectorAll('script[type="application/ld+json"]')]
              .map(s => {
                try { return JSON.parse(s.textContent); } catch { return null; }
              })
              .find(obj => obj && (obj.gtin13 || obj.sku || obj.name || obj.description));

            if (ldJson) {
              return {
                upc: ldJson.gtin13 || ldJson.sku || null,
                name: ldJson.name || null,
                description: ldJson.description || null,
              }
            };

            // 2️⃣ Fallback to __NEXT_DATA__
            const nextData = document.querySelector('script#__NEXT_DATA__');
            if (nextData) {
              const json = JSON.parse(nextData.textContent);
              const product = json?.props?.pageProps?.initialData?.data?.product || {};
              return {
                upc: product.upc || null,
                name: product.name || null,
                description: product.description || null,
              };
            }

            return { upc: null, name: null, description: null };
          } catch (err) {
            console.error("Failed to extract UPC:", err);
            return { upc: null, name: null, description: null };
          }
        },
      },
      async (injectionResults) => {
        if (chrome.runtime.lastError) {
          result.textContent = "Error: Unable to access page.";
          console.error(chrome.runtime.lastError.message);
          return;
        }

        const product = injectionResults?.[0]?.result;
        if (!product || (!product.upc && !product.name && !product.description)) {
          result.textContent = "No product info found on this page.";
          return;
        }

        result.textContent = `UPC: ${product.upc || "N/A"}\nName: ${product.name || "N/A"}\nDescription: ${product.description || "N/A"}`;
        await getRecommendation(product);
      }
    );
  });

  async function getRecommendation(product) {
    try {
      result.textContent = "Fetching recommendations...";
      // 🔹 Replace with your backend endpoint:
      // const response = await fetch(`https://your-backend-url.com/recommend?upc=${upc}`);
      // if (!response.ok) throw new Error(`Server returned ${response.status}`);
      // const data = await response.json();


    
      const request = { 
        "name": product.name,
        "description": product.description 
      }

      const data = await fetch("http://127.0.0.1:8000/qdrant", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(request)
      }).then(response => response.json());

      product = {
        "product_name": data.product_name,
        "snap_eligible": data.snap_eligible, 
        "price": data.price,
        "universal_product_code": data.universal_product_code,
        "product_URL": data.product_URL,
        "avg_rating": data.avg_rating,
        "image_url": data.image_url,
        "Nutrition_facts": {
          "calories": data.Nutrition_facts.calories,
          "total_fat_absolute": data.Nutrition_facts.total_fat_absolute,
          "total_fat_DV": data.Nutrition_facts.total_fat_DV,
          "sodium_absolute": data.Nutrition_facts.sodium_absolute,
          "sodium_DV": data.Nutrition_facts.sodium_DV,
          "total_carbs_absolute": data.Nutrition_facts.total_carbs_absolute,
          "total_carbs_DV": data.Nutrition_facts.total_carbs_DV,
          "total_sugars_absolute": data.Nutrition_facts.total_sugars_absolute,
          "protein_absolute": data.Nutrition_facts.protein_absolute,
          "ingredients": data.Nutrition_facts.ingredients,
          "ultraprocessed": data.Nutrition_facts.ultraprocessed,
          "category": data.Nutrition_facts.category
        }
      };
      
      // Mock sample data for now:
      // const data = {
      //   product_name: "Great Value 2% Reduced Fat Milk, Gallon, Refrigerated",
      //   snap_eligible: false,
      //   price: 3.46,
      //   universal_product_code: "078742351872",
      //   product_URL: "https://www.walmart.com/ip/Great-Value-2-Reduced-Fat-Milk-Gallon-Refrigerated/10450115",
      //   avg_rating: 4.4,
      //   image_url:
      //     "https://i5.walmartimages.com/seo/Great-Value-2-Reduced-Fat-Milk-Gallon-Refrigerated_22a6459a-13b6-4057-aeae-45e62c69e8f8.47f793426ff66fa6432c948d836704f0.jpeg",
      //   Nutrition_facts: {
      //     calories: "130",
      //     total_fat_absolute: "5g",
      //     total_fat_DV: "6%",
      //     sodium_absolute: "130mg",
      //     sodium_DV: "6%",
      //     total_carbs_absolute: "12g",
      //     total_carbs_DV: "4%",
      //     total_sugars_absolute: "12g",
      //     protein_absolute: "8g",
      //     ingredients: ["REDUCED FAT MILK", "VITAMIN A PALMITATE", "VITAMIN D3"],
      //     ultraprocessed: false,
      //   },
      // };

      displayRecommendation(product);
    } catch (err) {
      console.error(err);
      result.textContent = "❌ Failed to load recommendations.";
    }
  }

  function displayRecommendation(data) {
    const facts = data.Nutrition_facts || {};
    const snapEligible = data.snap_eligible ? "✅ SNAP Eligible" : "❌ Not SNAP Eligible";
    const processedTag = facts.ultraprocessed ? "⚠️ Ultraprocessed" : "🌿 Minimally Processed";

    result.innerHTML = `
      <div class="product-card">
        <a href="${data.product_URL}" target="_blank">
          <img src="${data.image_url}" alt="${data.product_name}" class="product-img" />
        </a>
        <div class="product-name">${data.product_name}</div>
        <div class="product-meta">
          $${data.price?.toFixed(2) ?? "N/A"} • ⭐ ${data.avg_rating ?? "N/A"}
        </div>
        <div>
          <span class="tag snap">${snapEligible}</span>
          <span class="tag processed">${processedTag}</span>
        </div>

        <div class="nutrition-section">
          <h3>Nutrition Facts</h3>
          <ul class="nutrition-list">
            <li><span>Calories</span><span>${facts.calories ?? "—"}</span></li>
            <li><span>Total Fat</span><span>${facts.total_fat_absolute ?? "—"} (${facts.total_fat_DV ?? ""})</span></li>
            <li><span>Sodium</span><span>${facts.sodium_absolute ?? "—"} (${facts.sodium_DV ?? ""})</span></li>
            <li><span>Total Carbs</span><span>${facts.total_carbs_absolute ?? "—"} (${facts.total_carbs_DV ?? ""})</span></li>
            <li><span>Total Sugars</span><span>${facts.total_sugars_absolute ?? "—"}</span></li>
            <li><span>Protein</span><span>${facts.protein_absolute ?? "—"}</span></li>
          </ul>
          <div class="ingredients">
            <strong>Ingredients:</strong> ${Array.isArray(facts.ingredients) ? facts.ingredients.join(", ") : "N/A"}
          </div>
        </div>
      </div>
    `;
  }
});