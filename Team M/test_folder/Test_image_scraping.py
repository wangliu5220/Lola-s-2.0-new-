import json
import pandas as pd
import re

# -------------------
# Helpers
# -------------------
def extract_number(value):
    """Extract numeric part from a cell (int/float/str). Returns as string."""
    if pd.isna(value):  # handle NaN
        return None
    value = str(value).strip()
    match = re.search(r"[\d.]+", value)
    return match.group() if match else None

# -------------------
# Load files
# -------------------
excel_path = "Team M/test_folder/test set.xlsx"
jsonl_path = "Team M/AI_Response.jsonl"

df = pd.read_excel(excel_path)
with open(jsonl_path, "r", encoding="utf-8") as f:
    jsonl_data = [json.loads(line) for line in f]

# Index JSONL by URL for quick lookup
jsonl_dict = {item["product_URL"]: item for item in jsonl_data}

# -------------------
# Compare values
# -------------------


def extract_numeric_value(value):
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    value_str = str(value).strip()
    match = re.search(r"\b\d*\.?\d+\b", value_str)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None

# ---------- Ingredients comparison ----------
def compare_ingredients(excel_ingredients, json_ingredients):
    if not excel_ingredients or not json_ingredients:
        return False
    
    # Ensure Excel value is a string
    excel_ingredients = str(excel_ingredients)
    
    # Normalize: lowercase, strip spaces, remove punctuation
    import string
    table = str.maketrans('', '', string.punctuation)
    
    excel_list = [x.strip().lower().translate(table) for x in excel_ingredients.split(',') if x.strip()]
    json_list = [x.strip().lower().translate(table) for x in json_ingredients if x.strip()]
    
    # Check if all Excel ingredients exist in JSON
    return all(any(ex in j for j in json_list) for ex in excel_list)

# ---------- Comparison ----------
for _, row in df.iterrows():
    url = row.get("product_URL")
    if url not in jsonl_dict:
        print("product not found")
        continue

    product = jsonl_dict[url]
    nutrition = product.get("Nutrition_facts", {})

    print(f"\nChecking product: {product['product_name']}")

    for col in df.columns:
        if col == "product_URL":
            continue

        excel_value = row[col]
        json_value = nutrition.get(col)

        if excel_value is None or json_value is None:
            continue

        # Ingredients special case
        if col.lower() == "ingredients":
            if compare_ingredients(excel_value, json_value):
                print(f"✅ {col}: Excel matches JSON")
            else:
                print(f"❌ {col}: Excel({excel_value}) not in JSON({json_value})")
            continue

        # Numeric comparison
        excel_num = extract_numeric_value(excel_value)
        json_num = extract_numeric_value(json_value)
        if excel_num is not None and json_num is not None:
            if excel_num == json_num:
                print(f"✅ {col}: Excel({excel_value}) matches JSON({json_value})")
            else:
                print(f"❌ {col}: Excel({excel_value}) not in JSON({json_value})")
        else:
            # fallback to string match
            if str(excel_value).strip().lower() in str(json_value).strip().lower():
                print(f"✅ {col}: Excel({excel_value}) matches JSON({json_value})")
            else:
                print(f"❌ {col}: Excel({excel_value}) not in JSON({json_value})")