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
snacks = [
    "snacks",
    "chips",
    "pretzels",
    "popcorn",
    "trail mix",
    "granola bars",
    "protein bars",
    "energy bars",
    "crackers",
    "rice cakes",
    "pita chips",
    "veggie chips",
    "snack mix",
    "cheese snacks",
    "nut snacks",
    "fruit snacks",
    "dried fruit",
    "jerky",
    "seaweed snacks",
    "snack packs",
    "cookies",
    "cupcakes",
    "brownies",
    "mini muffins",
    "pastries",
    "candy",
    "chocolate",
    "marshmallows",
    "low calorie snacks",
    "low sugar snacks",
    "gluten free snacks",
    "keto snacks",
    "vegan snacks",
    "protein snacks",
    "organic snacks",
    "non-GMO snacks",
    "spicy chips",
    "bbq chips",
]

frozen_foods = [
    "frozen foods",
    "frozen meals",
    "frozen sides",
    "frozen snacks",
    "frozen desserts",
    "frozen vegetables",
    "frozen mixed vegetables",
    "frozen broccoli",
    "frozen spinach",
    "frozen peas",
    "frozen corn",
    "frozen green beans",
    "frozen stir fry vegetables",
    "frozen cauliflower rice",
    "frozen fruit",
    "frozen berries",
    "frozen strawberries",
    "frozen blueberries",
    "frozen mango",
    "frozen pineapple",
    "frozen smoothie fruit",
    "frozen chicken",
    "frozen chicken breast",
    "frozen chicken nuggets",
    "frozen chicken tenders",
    "frozen chicken wings",
    "frozen beef",
    "frozen burgers",
    "frozen meatballs",
    "frozen sausage",
    "frozen seafood",
    "frozen shrimp",
    "frozen salmon",
    "frozen fish fillets",
    "frozen crab cakes",
    "frozen pizza",
    "frozen thin crust pizza",
    "frozen deep dish pizza",
    "frozen pepperoni pizza",
    "frozen cheese pizza",
    "frozen vegetable pizza",
    "frozen gluten free pizza",
    "frozen pasta",
    "frozen lasagna",
    "frozen ravioli",
    "frozen macaroni and cheese",
    "frozen rice meals",
    "frozen Asian meals",
    "frozen Mexican meals",
    "frozen Indian meals",
    "frozen vegetarian meals",
    "frozen vegan meals",
    "frozen low calorie meals",
    "frozen high protein meals",
    "frozen waffles",
    "frozen pancakes",
    "frozen french toast sticks",
    "frozen breakfast sandwiches",
    "frozen breakfast burritos",
    "frozen hash browns",
    "frozen tater tots",
    "frozen breakfast bowls",
    "frozen ice cream",
    "frozen ice cream bars",
    "frozen popsicles",
    "frozen fruit bars",
    "frozen yogurt",
    "frozen yogurt bars",
    "frozen sorbet",
    "frozen gelato",
    "frozen dairy free ice cream",
    "frozen keto ice cream",
    "frozen pies",
    "frozen cakes",
    "frozen cheesecakes",
    "frozen cookie dough",
    "gluten free frozen foods",
    "keto frozen foods",
    "low carb frozen foods",
    "vegan frozen foods",
    "vegetarian frozen foods",
    "organic frozen foods",
    "non-GMO frozen foods",
]

bakery = [
    "bakery",
    "fresh bakery",
    "bread",
    "rolls",
    "bagels",
    "croissants",
    "buns",
    "tortillas",
    "flatbreads",
    "pita bread",
    "naan bread",
    "artisan bread",
    "whole wheat bread",
    "multigrain bread",
    "white bread",
    "rye bread",
    "sourdough bread",
    "gluten free bread",
    "organic bread",
    "cakes",
    "birthday cakes",
    "sheet cakes",
    "cupcakes",
    "cake slices",
    "brownies",
    "bars",
    "cheesecake",
    "pies",
    "fruit pies",
    "apple pie",
    "cherry pie",
    "pumpkin pie",
    "pecan pie",
    "cookies",
    "chocolate chip cookies",
    "sugar cookies",
    "oatmeal cookies",
    "gingerbread cookies",
    "shortbread cookies",
    "sandwich cookies",
    "donuts",
    "glazed donuts",
    "chocolate donuts",
    "powdered donuts",
    "filled donuts",
    "danishes",
    "pastries",
    "turnovers",
    "strudels",
    "eclairs",
    "cream puffs",
    "muffins",
    "blueberry muffins",
    "chocolate chip muffins",
    "banana muffins",
    "mini muffins",
    "sweet rolls",
    "cinnamon rolls",
    "sticky buns",
    "savory rolls",
    "stuffed bread",
    "breadsticks",
    "garlic bread",
    "focaccia",
    "holiday cakes",
    "holiday cookies",
    "pumpkin bread",
    "zucchini bread",
    "banana bread",
    "fruit bread",
    "panettone",
    "hot cross buns",
    "king cake",
    "low calorie baked goods",
    "sugar free baked goods",
    "gluten free baked goods",
    "vegan baked goods",
    "keto baked goods",
    "organic baked goods",
]
deli = [
    "deli",
    "prepared foods",
    "grab and go",
    "ready to eat meals",
    "ready to eat snacks",
    "ready to eat lunch",
    "ready to eat dinner",
    "meal kits",
    "fresh deli meals",
    "deli sandwiches",
    "grab and go sandwiches",
    "turkey sandwich",
    "ham sandwich",
    "chicken sandwich",
    "club sandwich",
    "wraps",
    "chicken wrap",
    "turkey wrap",
    "veggie wrap",
    "deli salads",
    "pasta salad",
    "potato salad",
    "coleslaw",
    "chicken salad",
    "egg salad",
    "tuna salad",
    "garden salad",
    "caesar salad",
    "chef salad",
    "fruit salad",
    "side salads",
    "rotisserie chicken",
    "fried chicken",
    "chicken tenders",
    "chicken wings",
    "hot meals",
    "mac and cheese deli",
    "mashed potatoes deli",
    "meatloaf deli",
    "grilled chicken deli",
    "prepared pasta dishes",
    "snack packs",
    "protein snack packs",
    "cheese snack packs",
    "meat and cheese snack packs",
    "cracker snack packs",
    "fruit snack packs",
    "veggie snack packs",
    "hummus and pretzels snack packs",
    "sliced deli meat",
    "sliced turkey",
    "sliced ham",
    "sliced roast beef",
    "sliced chicken breast",
    "salami",
    "pepperoni",
    "prosciutto",
    "deli cheese",
    "sliced cheddar cheese",
    "sliced american cheese",
    "sliced swiss cheese",
    "sliced provolone cheese",
    "sliced mozzarella cheese",
    "organic deli foods",
    "gluten free deli foods",
    "keto deli foods",
    "low sodium deli meat",
    "vegan deli slices",
    "plant based deli meat",
    "plant based prepared meals",
    "vegetarian grab and go",
]
pantry = [
    "pantry",
    "dry goods",
    "pantry staples",
    "non perishable foods",
    "shelf stable foods",
    "canned vegetables",
    "canned corn",
    "canned green beans",
    "canned peas",
    "canned mushrooms",
    "canned tomatoes",
    "diced tomatoes",
    "tomato paste",
    "tomato sauce",
    "canned beans",
    "black beans",
    "kidney beans",
    "pinto beans",
    "chickpeas",
    "baked beans",
    "canned fruit",
    "canned peaches",
    "canned pineapple",
    "canned pears",
    "canned mandarin oranges",
    "canned mixed fruit",
    "applesauce cups",
    "fruit cups",
    "canned soups",
    "chicken noodle soup",
    "tomato soup",
    "vegetable soup",
    "cream of mushroom soup",
    "broth",
    "chicken broth",
    "beef broth",
    "vegetable broth",
    "pasta",
    "spaghetti",
    "macaroni",
    "penne",
    "gluten free pasta",
    "whole wheat pasta",
    "rice",
    "white rice",
    "brown rice",
    "jasmine rice",
    "basmati rice",
    "wild rice",
    "instant rice",
    "quinoa",
    "couscous",
    "barley",
    "oats",
    "rolled oats",
    "instant oats",
    "oatmeal packets",
    "baking ingredients",
    "flour",
    "all purpose flour",
    "whole wheat flour",
    "almond flour",
    "sugar",
    "brown sugar",
    "powdered sugar",
    "baking soda",
    "baking powder",
    "cornmeal",
    "cornstarch",
    "cocoa powder",
    "chocolate chips",
    "cake mix",
    "brownie mix",
    "pancake mix",
    "syrup",
    "condiments",
    "ketchup",
    "mustard",
    "mayonnaise",
    "hot sauce",
    "soy sauce",
    "teriyaki sauce",
    "bbq sauce",
    "pasta sauce",
    "marinara sauce",
    "alfredo sauce",
    "peanut butter",
    "almond butter",
    "jelly",
    "jam",
    "honey",
    "maple syrup",
    "cooking oil",
    "olive oil",
    "vegetable oil",
    "canola oil",
    "coconut oil",
    "seasonings",
    "salt",
    "pepper",
    "garlic powder",
    "onion powder",
    "italian seasoning",
    "chili powder",
    "curry powder",
    "spices",
    "herbs",
    "cereal",
    "granola",
    "instant oatmeal",
    "pancake mix",
    "waffle mix",
    "organic pantry foods",
    "gluten free pantry foods",
    "vegan pantry foods",
    "keto pantry foods",
    "low sodium canned goods",
    "sugar free pantry items",
]

breakfast = [
    "breakfast foods",
    "cereal",
    "granola",
    "oatmeal",
    "grits",
    "breakfast bars",
    "granola bars",
    "protein bars",
    "energy bars",
    "pancake mix",
    "waffle mix",
    "jam",
    "jelly",
    "nut butter",
    "peanut butter",
    "almond butter",
    "bagels",
    "english muffins",
    "croissants",
    "muffins",
    "donuts",
    "pastries",
    "breakfast sandwiches",
    "eggs",
    "bacon",
    "sausage",
    "hash browns",
    "breakfast potatoes",
    "yogurt",
    "greek yogurt",
    "cottage cheese",
    "smoothies",
    "protein shakes",
    "breakfast drinks",
]


search_queries = breakfast

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
    "https://www.walmart.com/ip/Coca-Cola-Mini-Soda-Pop-Fridge-Pack-7-5-fl-oz-Cans-10-Pack/125411280?athcpid=125411280&athpgid=AthenaContentPage_1001680&athcgid=null&athznid=ItemCarousel_8ae3b15c-272e-48e9-a6d9-111bb0c0fec6_items&athieid=v0&athstid=CS020&athguid=pLBLMGla_h7pLBbMmVflw37iNPPYmwonI6pw&athancid=null&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Diet-Dr-Pepper-Soda-Pop-2-L-Bottle/16940508?classType=REGULAR&athbdg=L1600&from=/search",
    "https://www.walmart.com/ip/Great-Value-2-Reduced-Fat-Milk-Gallon-Refrigerated/10450115?classType=REGULAR&athbdg=L1600",
    "https://www.walmart.com/ip/Shamrock-Farms-Lactose-Free-Rockin-Protein-Builder-Chocolate-12-fl-oz-Bottle/21685899?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Great-Value-1-Low-fat-Chocolate-Milk-Gallon-Plastic-Jug-128-Fl-Oz/17248403?classType=REGULAR",
    "https://www.walmart.com/ip/Chobani-Oatmilk-Zero-Sugar-Unsweetened-52-fl-oz/5853809550?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Polar-Zero-Calorie-Lime-Sparkling-Seltzer-Water-12-fl-oz-8-Pack-Cans/505115147?athcpid=505115147&athpgid=AthenaItempage&athcgid=null&athznid=ci&athieid=v0&athstid=CS055~CS004&athguid=vKhIvxPOHnjgNeX52pvNkwNxzs2n61T8K4MU&athancid=5853809550&athposb=0&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Synergy-The-Real-Kombucha-Gingerade-16-fl-oz/51259259?adsRedirect=true",
    "https://www.walmart.com/ip/Tropicana-Classic-Lemonade-Made-with-Real-Lemons-46-fl-oz-Bottle/5349984438?adsRedirect=true",
    "https://www.walmart.com/ip/Java-Monster-Loca-Moca-Coffee-Energy-Drink-11-fl-oz-6pk/957052004?classType=VARIANT",
    "https://www.walmart.com/ip/TAZO-Matcha-Latte-Green-Tea-32-oz-Carton/20709848?athcpid=20709848&athpgid=AthenaContentPage_1001320&athcgid=null&athznid=ItemCarousel_e2140114-d4e9-4603-b21f-e29c3b7295e0_items&athieid=v0&athstid=CS020&athguid=eaycUWOVh2Pm-BCcvGqIqC0SOfCp8FikdbBr&athancid=null&athena=true",
    "https://www.walmart.com/ip/Vita-Coco-Pure-Coconut-Water-1-Liter/34789040?classType=VARIANT&athbdg=L1200",
    "https://www.walmart.com/ip/4-pack-Jumex-Mango-Nectar-from-Concentrate-11-3-Fl-oz/14762319347?classType=VARIANT&from=/search",
    "https://www.walmart.com/ip/OLIPOP-Prebiotic-Soda-Classic-Root-Beer-12-fl-oz-4-Pack-Pantry-Packs/6925153849?athcpid=6925153849&athpgid=AthenaItempage&athcgid=null&athznid=si&athieid=v0_eeMzkuNDQsNjk1Mi4yOSwwLjAwNTk3MjUxNjEyNjQxMjc4LDAuNV8_cuW3siYnIiOnsiYXRocnMiOjAuMCwiYXRocyI6MC4wfSwiZm4iOnsiYXRocyI6MC4wMDIzNDExNjYzMTI4NTc2MjF9LCAiYnJ2IjoiaHYxIn1d&athstid=CS055~CS004&athguid=G05xzTAehwvmP8DiRc6LQBueJdEEGzTyKEEf&athancid=2292221250&athposb=0&athena=true",
    "https://www.walmart.com/ip/Carnation-Breakfast-Essentials-Nutritional-Protein-Packed-Drink-Shakes-Rich-Milk-Chocolate-8-fl-oz-6-Pack/34259082?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Starbucks-Frappuccino-White-Chocolate-Mocha-Iced-Coffee-Drink-13-7-fl-oz-12-Pack-Bottles/2601000072?classType=VARIANT&adsRedirect=true",
    "https://www.walmart.com/ip/Horizon-Organic-High-Vitamin-D-Whole-Milk-High-Vitamin-D-Whole-64-fl-oz-Carton/10309701?classType=REGULAR&adsRedirect=true",
    "https://www.walmart.com/ip/Great-Value-Mountain-Lightning-Citrus-Flavored-Soda-Pop-2-Liter-Bottle/35506012?athcpid=35506012&athpgid=AthenaContentPage_1001680&athcgid=null&athznid=ItemCarousel_90ce338a-ba50-419c-9341-6f8b72233362_items&athieid=v0&athstid=CS020&athguid=XXpkw5cFGtHtrIZBtYxDCJwUfO2RmrkrAo7p&athancid=null&athena=true&athbdg=L1300",
    "https://www.walmart.com/ip/Culture-Pop-Soda-Watermelon-Probiotic-Soda-12-fl-oz/436428978?classType=REGULAR&athbdg=L1200&adsRedirect=true",
    "https://www.walmart.com/ip/Minute-Maid-No-Pulp-Orange-Fruit-Juice-59-fl-oz-Carton/22176380?athcpid=22176380&athpgid=AthenaItempage&athcgid=null&athznid=si&athieid=v0_eeMzcuNDYsMzM4Mi4yNzk5OTk5OTk5OTk3LDAuMDExMDY5OTAwOTQ0NzYzMDEzLDAuNV8_cuW3siYnIiOnsiYXRocnMiOjAuMCwiYXRocyI6MC4wfSwiZm4iOnsiYXRocyI6MC4wMDM2Nzc5NDI1ODkzOTAwNjYzfSwgImJydiI6Imh2MSJ9XQ&athstid=CS055~CS004&athguid=YYimtgCgkzgTN6D3gmzsxxu_P6FfOQzOmcZJ&athancid=13689271530&athposb=0&athena=true&athbdg=L1600",
    "https://www.walmart.com/ip/Sparkling-Ice-Naturally-Flavored-Sparkling-Water-Black-Raspberry-17-fl-oz/21268881?adsRedirect=true",
    "https://www.walmart.com/ip/Sanzo-Lychee-Sparkling-Water-12-Cans-Made-with-Real-Fruit-No-Added-Sugar-Carbonated-Water-Flavored/9247067342?adsRedirect=true",
    "https://www.walmart.com/ip/Core-Power-Protein-Shake-with-26g-Protein-by-fairlife-Milk-Vanilla-14-fl-oz/822766999?classType=VARIANT&athbdg=L1102&from=/search"
    ]
    OUTPUT_FILE="Team M/test_folder/result_from_1.jsonl"
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
    OUTPUT_FILE = "Team M/result_from_1.jsonl"
    CACHE_FILE = "Team M/cache_part_1.jsonl"
    SCRAPE_LIMIT = -1  # Adjust as needed

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
                        if counter >= SCRAPE_LIMIT and SCRAPE_LIMIT != -1:
                            print("Scrape limit reached")
                            break
                    except Exception as e:
                        print(f"Failed to process {product_url}: {e}")
                else:
                    page_number += 1
                    if(page_number > 99):
                        print("Page limit reached 99")
                        break
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
