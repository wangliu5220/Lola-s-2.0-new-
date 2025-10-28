from bs4 import BeautifulSoup
import requests
import json
import link_scrape
import queue
import os

# Base Walmart URL
WALMART_URL = "https://www.walmart.com/"

# HTTP headers
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
    "referer": WALMART_URL
}

# Search queries
search_queries = [
    "fresh fruits",
    "fresh vegetables",
    "meat",
    "poultry",
    "fresh fish",
    "fresh seafood",
    "steaks",
    "fresh chicken"
]

# Queue and seen URLs
product_queue = queue.Queue()
seen_urls = set()

def extract_product_info(product_url, cache):
    """Extract Walmart product info with caching."""
    if product_url in cache:
        return cache[product_url]

    try:
        response = requests.get(product_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Request failed for {product_url}: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    script_tag = soup.find("script", id="__NEXT_DATA__")
    if not script_tag or not script_tag.string:
        return None

    try:
        data = json.loads(script_tag.string)
    except json.JSONDecodeError:
        return None

    initial_data = (
        data.get("props", {})
            .get("pageProps", {})
            .get("initialData", {})
            .get("data", {})
    )

    product_data = initial_data.get("product", {})
    reviews_data = initial_data.get("reviews", {})
    nutrition_data = initial_data.get("idml", {}).get("nutritionFacts", {})

    product_info = {
        "product_name": product_data.get("name", ""),
        "snap_eligible": product_data.get("snapEligible", False),
        "short_description": product_data.get("shortDescription", ""),
        "price": product_data.get("priceInfo", {}).get("currentPrice", {}).get("price", "not found"),
        "universal_product_code": product_data.get("upc", ""),
        "product_URL": product_url,
        "avg_rating": reviews_data.get("averageOverallRating", 0),
        "review_count": reviews_data.get("totalReviewCount", 0),
        "item_id": product_data.get("usItemId", ""),
        "brand": product_data.get("brand", ""),
        "availability": product_data.get("availabilityStatus", ""),
        "type": product_data.get("type", ""),
        "zip_code": product_data.get("location", {}).get("postalCode", ""),
    }

    # Breadcrumbs
    bread_crumbs = initial_data.get("seoItemMetaData", {}).get("breadCrumbs", [])
    for i, category in enumerate(bread_crumbs, start=1):
        product_info[f"dep/cat/shelf{i}"] = category.get("name", "")

    # Serving info
    serving_info = nutrition_data.get("servingInfo", {}).get("values", [])
    if serving_info:
        for s in serving_info:
            product_info[s.get("name", "serving_info")] = s.get("value", "0")
    else:
        product_info["serving_information"] = "not found"

    # Calories
    calorie_info = nutrition_data.get("calorieInfo", {}).get("mainNutrient", {})
    product_info["calories"] = calorie_info.get("amount", "not found")

    # Key nutrients
    key_nutrients = nutrition_data.get("keyNutrients", {}).get("values", [])
    if key_nutrients:
        for key_nutr_val in key_nutrients:
            main = key_nutr_val.get("mainNutrient", {})
            name = main.get("name", "")
            if name:
                product_info[f"{name}_amount"] = main.get("amount", "0")
                product_info[f"{name}_dvp"] = main.get("dvp", "0")
            for child in key_nutr_val.get("childNutrients", []) or []:
                cname = child.get("name", "")
                product_info[f"{cname}_amount"] = child.get("amount", "0")
                product_info[f"{cname}_dvp"] = child.get("dvp", "0")
    else:
        product_info["key_nutrients"] = "not found"

    # Vitamins
    vitamins = nutrition_data.get("vitaminMinerals", {}).get("childNutrients", [])
    if vitamins:
        for v in vitamins:
            vname = v.get("name", "")
            product_info[f"{vname}_amount"] = v.get("amount", "0")
            product_info[f"{vname}_dvp"] = v.get("dvp", "0")
    else:
        product_info["vitamin_minerals"] = "not found"

    # Ingredients
    product_info["ingredients"] = (
        initial_data.get("idml", {})
        .get("ingredients", {})
        .get("ingredients", {})
        .get("value", "not found")
    )

    # Images
    image_info = product_data.get("imageInfo", {})
    if image_info:
        product_info["thumbnail_image_url"] = image_info.get("thumbnailUrl", "")
        for i, image in enumerate(image_info.get("allImages", []), start=1):
            product_info[f"image_url_{i}"] = image.get("url", "")

    cache[product_url] = product_info
    return product_info



def processFromUrls( SCRAPE_LIMIT=100):
    urls = [
    "https://www.walmart.com/ip/Fresh-Honeycrisp-Apple-Each/44390950?classType=REGULAR&from=/search"
    ]
    OUTPUT_FILE="Non-Beverage Scrape/test_data.jsonl"
    CACHE_FILE="Team M/test_folder/cache_part_1.jsonl"
    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    cache[item.get("product_URL", "")] = item
                except json.JSONDecodeError:
                    continue
        print(f"Loaded {len(cache)} items from cache")
    else:
        print("No cache found, starting fresh")

    # Add new URLs to queue
    for url in urls:
        if url not in seen_urls:
            product_queue.put(url)
            seen_urls.add(url)

    counter = 0
    with open(OUTPUT_FILE, "a") as f:
        while not product_queue.empty():
            product_url = product_queue.get()
            try:
                product_info = extract_product_info(product_url, cache)
                if product_info:
                    print(f"Writing product: {product_info.get('product_name', 'UNKNOWN')}")
                    f.write(json.dumps(product_info) + "\n")
                    f.flush()
                    counter += 1
                else:
                    print("No product info extracted")

                if counter >= SCRAPE_LIMIT:
                    print("Scrape limit reached")
                    break
            except Exception as e:
                print(f"Failed to process {product_url}: {e}")

    # Save updated cache
    with open(CACHE_FILE, "w") as f_cache:
        for item in cache.values():
            f_cache.write(json.dumps(item) + "\n")

    print("Scraping completed.")


def main():
    OUTPUT_FILE = "Non-Beverage Scrape/test_data.jsonl"
    CACHE_FILE = "Team M/cache_part_1.jsonl"
    SCRAPE_LIMIT = 200  # Adjust as needed

    # Load cache
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    cache[item.get("product_URL", "")] = item
                except json.JSONDecodeError:
                    continue
        print(f"Loaded {len(cache)} items from cache")
    else:
        print("No cache found, starting fresh")

    counter = 0
    with open(OUTPUT_FILE, "a") as f:
        for query in search_queries:
            print(f"\nProcessing search query: {query}\n")
            page_number = 1
            while True:
                links = link_scrape.get_product_links_from_search_page(query, page_number)
                if page_number > 6:
                    break
                if not links:
                    break
                print(f"Found {len(links)} links on page {page_number}")

                for link in links:
                    if link not in seen_urls:
                        product_queue.put(link)
                        seen_urls.add(link)

                while not product_queue.empty():
                    product_url = product_queue.get()
                    try:
                        product_info = extract_product_info(product_url, cache)
                        if product_info:
                            print(f"Writing product: {product_info.get('product_name', 'UNKNOWN')}")
                            f.write(json.dumps(product_info) + "\n")
                            f.flush()
                            counter += 1
                        else:
                            print("No product info extracted")
                        if counter >= SCRAPE_LIMIT:
                            print("Scrape limit reached")
                            break
                    except Exception as e:
                        print(f"Failed to process {product_url}: {e}")
                else:
                    page_number += 1
                    continue
                break

    # Save cache
    with open(CACHE_FILE, "w") as f_cache:
        for item in cache.values():
            f_cache.write(json.dumps(item) + "\n")

    print("Scraping completed.")

if __name__ == "__main__":
    # processFromUrls()
    main()
