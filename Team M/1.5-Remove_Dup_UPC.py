import json

input_path = "Team M/result_from_1.jsonl"
output_path = "Team M/result_deduped.jsonl"

seen_upcs = set()
deduped = []

with open(input_path, "r", encoding="utf-8") as infile:
    for line in infile:
        line = line.strip()
        if not line:
            continue
        try:
            product = json.loads(line)
        except json.JSONDecodeError:
            print("⚠️ Skipping malformed line.")
            continue

        upc = product.get("universal_product_code")
        if not upc:
            # Optionally skip or include products without UPC
            print(f"⚠️ Skipping item with missing UPC: {product.get('product_name')}")
            continue

        if upc not in seen_upcs:
            seen_upcs.add(upc)
            deduped.append(product)
        else:
            print(f"🔁 Duplicate UPC found: {upc} — skipping {product.get('product_name')}")

# Write out deduplicated results
with open(output_path, "w", encoding="utf-8") as outfile:
    for product in deduped:
        outfile.write(json.dumps(product, ensure_ascii=False) + "\n")

print(f"✅ Deduplicated file saved to: {output_path}")
print(f"🧾 Unique UPC count: {len(seen_upcs)}")
