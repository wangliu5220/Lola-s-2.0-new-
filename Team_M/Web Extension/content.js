// 🧩 Extract UPC from page (ld+json or __NEXT_DATA__)
function extractProduct() {
  try {
    const ldJson = [...document.querySelectorAll('script[type="application/ld+json"]')]
      .map(s => { try { return JSON.parse(s.textContent); } catch { return null; } })
      .find(obj => obj && (obj.gtin13 || obj.sku || obj.name || obj.description));

    if (ldJson) {
      return {
        upc: ldJson.gtin13 ?? ldJson.sku ?? null,
        name: ldJson.name ?? null,
        description: ldJson.description ?? null,
      }
    };

    const script = document.querySelector('script#__NEXT_DATA__');
    if (script) {
      const json = JSON.parse(script.textContent);
      const product = json?.props?.pageProps?.initialData?.data?.product || {};
      
      if (product) {
        return {
            upc: product.upc ?? null,
            name: product.name ?? null,
            description: product.description ?? null,
          };
        }
      }

    return null;
  } catch (err) {
    console.error("❌ Failed to extract UPC:", err);
    return null;
  }
}

// 🪣 Inject or update recommendation box
function insertBox(html = "⏳ Loading Lola’s 2.0…") {
  let box = document.getElementById("walmart-extension-box");
  if (!box) {
    const target = document.querySelector('div[data-testid="add-to-cart-section"]');
    if (!target) {
      console.warn("⚠️ Target not found for insertBox()");
      return;
    }
    box = document.createElement("div");
    box.id = "walmart-extension-box";
    target.prepend(box);
  }
  box.innerHTML = html;
  Object.assign(box.style, {
    backgroundColor: "#f5f9f4",
    border: "1px solid #a5c6a1",
    borderRadius: "10px",
    color: "#2a3b2a",
    padding: "10px",
    marginTop: "12px",
    fontFamily: '"Inter","Segoe UI",sans-serif',
    width: "100%",
    boxSizing: "border-box",
  });
}

// 🧠 Mock backend call with 5-second delay
function queryBackendAndUpdateUI(product) {
  // Show loading state
  insertBox("⏳ Fetching recommendations...");

  const request = {
    name: product?.name || null,
    description: product?.description || null,
  };

  fetch("http://127.0.0.1:8000/qdrant", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  })
    .then((response) => {
      if (!response.ok) throw new Error(`Server returned ${response.status}`);
      return response.json();
    })
    .then((data) => {
      data = data.best_match;

      const nf = data?.Nutrition_facts ?? {};
      const recommendation = {
        product_name: data?.product_name ?? "N/A",
        snap_eligible: data?.snap_eligible ?? false,
        price: typeof data?.price === "number" ? data.price : 0,
        universal_product_code: data?.universal_product_code || product?.upc || null,
        product_URL: data?.product_URL || "#",
        avg_rating: data?.avg_rating ?? "N/A",
        image_url: data?.image_url || "N/A",
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
          ultraprocessed: nf.ultraprocessed ?? "N/A",
          category: nf.category ?? "N/A",
        },
      };

      insertBox(`
        <div style="display:flex;align-items:center;gap:10px;">
          <img src="${recommendation.image_url}" style="width:60px;height:60px;border-radius:8px;object-fit:cover;" />
          <div style="flex:1;">
            <div style="font-weight:600;color:#2f4f2f;">${recommendation.product_name}</div>
            <div style="font-size:14px;color:#3b3b3b;">$${(recommendation.price || 0).toFixed(2)} • ⭐ ${recommendation.avg_rating}</div>
            <div style="font-size:13px;color:#3b3b3b;">
              <b>Calories:</b> ${recommendation.Nutrition_facts.calories} |
              <b>Protein:</b> ${recommendation.Nutrition_facts.protein_absolute} |
              <b>Fat:</b> ${recommendation.Nutrition_facts.total_fat_absolute}
            </div>
            <div style="margin-top:6px;">
              <a href="${recommendation.product_URL}" target="_blank"
                style="color:#2f4f2f;text-decoration:underline;font-weight:500;">
                View Product
              </a>
            </div>
          </div>
        </div>
      `);
    })
    .catch((err) => {
      console.error("Failed to fetch recommendations:", err);
      insertBox("Recommendations Unavailable");
    });

  

  // setTimeout(() => {
  //   console.log("✅ Updating UI for", upc);
  //   // We call the actual here. 
  //   const data = {
  //     product_name: "Great Value Milk Whole Vitamin D, Half Gallon, Plastic, Jug, 64oz",
  //     "snap_eligible": false,
  //     "price": 2.06,
  //     "universal_product_code": "078742352008",
  //     "product_URL": "https://www.walmart.com/ip/Great-Value-Milk-Whole-Vitamin-D-Half-Gallon-Plastic-Jug-64oz/10450118?classType=REGULAR&athbdg=L1600&from=/search",
  //     "avg_rating": 4.3,
  //     "Nutrition_facts": {
  //       "servings_per_container": "8",
  //       "serving_size": "1 cup (240mL)",
  //       "calories": "150",
  //       "total_fat_absolute": "8g",
  //       "total_fat_DV": "10%",
  //       "sodium_absolute": "125mg",
  //       "sodium_DV": "5%",
  //       "total_carbs_absolute": "12g",
  //       "total_carbs_DV": "4%",
  //       "protein_absolute": "8g",
  //       "protein_DV": "16%",
  //       "cholesterol_absolute": "35mg",
  //       "cholesterol_DV": "12%",
  //       "saturated_fat_absolute": "5g",
  //       "saturated_fat_DV": "25%",
  //       "ingredients": ["MILK", "VITAMIN D3"],
  //       "ultraprocessed": false,
  //       "category": "Dairy",
  //     },
  //     "image_url": "https://i5.walmartimages.com/seo/Great-Value-Milk-Whole-Vitamin-D-Half-Gallon-Plastic-Jug-64oz_52ec45c4-586d-42c0-a42c-93218631e277.ec8d19bdf634f97445cbf455eac874a8.jpeg"
  //   };

  //   insertBox(`
  //     <div style="display:flex;align-items:center;gap:10px;">
  //       <img src="${data.image_url}" style="width:60px;height:60px;border-radius:8px;object-fit:cover;" />
  //       <div style="flex:1;">
  //         <div style="font-weight:600;color:#2f4f2f;">${data.product_name}</div>
  //         <div style="font-size:14px;color:#3b3b3b;">$${data.price.toFixed(2)} • ⭐ ${data.avg_rating}</div>
  //         <div style="font-size:13px;color:#3b3b3b;">
  //           <b>Calories:</b> ${data.Nutrition_facts.calories} |
  //           <b>Protein:</b> ${data.Nutrition_facts.protein_absolute} |
  //           <b>Fat:</b> ${data.Nutrition_facts.total_fat_absolute}
  //         </div>
  //         <div style="margin-top:6px;">
  //           <a href="${data.product_URL}" target="_blank"
  //             style="color:#2f4f2f;text-decoration:underline;font-weight:500;">
  //             View Product
  //           </a>
  //         </div>
  //       </div>
  //     </div>
  //   `);
  // }, 5000);
}

// 🔁 Watcher to auto-restart on UPC or route change
function initUPCWatcher() {
  console.log("👀 Starting Walmart UPC watcher...");

  // Run on initial load
  const product = extractProduct();
  queryBackendAndUpdateUI(product);

  // ✅ Hook into Next.js router events (no full reload)
  const router = window.next?.router;
  if (router) {
    router.events.on("routeChangeComplete", (url) => {
      console.log("🔄 Walmart route changed:", url);
      setTimeout(() => {
        const product = extractProduct();
        queryBackendAndUpdateUI(product);
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
          const product = extractProduct();
          queryBackendAndUpdateUI(product);
        }, 1200);
      }
    });
    observer.observe(document.body, { childList: true, subtree: true });
  }
}

initUPCWatcher();