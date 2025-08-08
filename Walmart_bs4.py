#For scraping off multiple item information off of walmart using search query 
#based off repo from keith galli 

from bs4 import BeautifulSoup
import requests
import json
import link_scrape
import queue
import os

walmart_url = "https://www.walmart.com/"

# not sure if this is obtaining the data from the correct zip code
# might have to add cookies or add some type of proxy system? Proxy would cost money 
# sometimes gets captcha 307/402 but I think using a vpn works? long term issue and will either have to implement a proxy or find some other method
# sometimes changing the headers content or changing what headers are included works as well
HEADERS = {
    # "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    # "accept": "*/*",
    # "accept-language": "en-US,en;q=0.9",
    # "accept-encoding": "gzip, deflate, br, zstd",
    # "referer": "https://www.walmart.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "en-US",
    "accept-encoding": "gzip, deflate, br, zstd",
    "referer": "https://www.walmart.com/"

}

# List of search queries
search_queries = [
    # "beverages",
    # "milk",
    # "drinks",
    # "coffee",
    # "sparkling water",
    # "water",
    # "juice",
    # "tea",
    # "soda",
    # "energy drinks",
    # "fruit juice",
    # "fruit punch juice",
    # "sports drinks",
    # "flavored water",
    # "mineral water",
    # "spring water",
    # "purified water",
    # "distilled water",
    # "bottled water",
    # "iced tea",
    # "lemonade",
    # "kombucha",
    # "probiotic drinks",
    # "plant-based milk",
    # "dairy-free milk",
    # "lactose-free milk",
    # "mocha",
    # "latte",
    # "espresso",
    # "iced coffee",
    # "coffee creamer",
    # "coffee syrup",
    # "hot chocolate",
    # "chocolate milk",
    # "smoothie",
    # "cola",
    # "diet soda",
    # "root beer",
    # "ginger ale",
    # "cream soda",
    # "tonic water",
    # "club soda",
    # "orange soda",
    # "grape soda",
    # "lemon-lime soda",
    # "fruit soda",
    # "berry soda",
    # "vanilla soda",
    # "cherry soda",
    # "sugar-free soda",
    # "sweet tea",
    # "bubble tea",
    # "milkshake",
    # "fruit flavor",
    # "milk drinks",
    # "milk beverages",
    # "fruit flavor sparkling water",
    # "fruit punch",
    # "dairy drinks",
    # "yogurt drink",
    # "non sweet tea",
    # "iced sweet tea",
    # "fruit punch soda",
    # "fruit punch juice",
    # "fruit punch flavor sparkling water",
    # "fruit flavor sparkling water",
    # "fruit flavor sparkling water with real fruit",
    "fruit flavor sparkling water with natural flavors",
    "fruit flavor sparkling water with artificial flavors",
    "fruit flavor sparkling water with no added sugar",
    "fruit flavor sparkling water with no added calories",
    "fruit flavor sparkling water with antioxidant",
]

# Initialize a queue for product URLs and a set for seen URLs
product_queue = queue.Queue()
seen_urls = set()
    

def extract_product_info(product_url, cache):
    """_summary_

    Args:
        product_url (string): full url of product to be extracted
        id_list (list): list of item UPC's

    Returns:
        product_info: dictionary of a single items nutrition and sale information
        
    department, aisle, shelf, name, images, price,
    ingredients, serving size, servings per container,
    calories, total fat, trans fat, saturated fat, sodium, 
    carbohydrates, fiber, sugar, protein, iron, shelf rank.
    
    accounted for:
    serving per container, serving size, potassium, calcium, vitamin c, 
    vitamin a, protein, total carbs, dietary fiber, sugars, added sugars,
    sodium, cholesterol, total fat, calories, transfat, saturated fat, iron, image
    price, review count, average review, item id, product description, 
    brand, name, type, ingredients, department, aisle, shelf
   
    missing: 
        shelf rank, snap eligibility    
    """
    print("in extract_product_info")
    
    # if str(product_url) in cache:
    if cache.get(product_url) != None:
        print("Product already in cache")
        return cache[product_url]
    # have to manually add in new data to cache after program runs (been to lazy to write it into the code...)
    
    response = requests.get(product_url, headers=HEADERS)
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    script_tag = soup.find("script", id="__NEXT_DATA__")
    data = json.loads(script_tag.string)
     

    initial_data = data["props"]["pageProps"]["initialData"]["data"]
    product_data = initial_data["product"]
    reviews_data = initial_data.get("reviews", {})
    nutrition_data = initial_data['idml']
    
    
    product_info = {
        #product information, use product_data tag or other appropriate tag
        "product_name": product_data["name"],
        "snap_eligible" : product_data.get("snapEligible", False),
        "short_description": product_data.get("shortDescription", ""),
        "price": product_data["priceInfo"]["currentPrice"]["price"],
        "universal_product_code": product_data.get("upc", ""),
        "product_URL" : product_url,    
        "avg_rating": reviews_data.get("averageOverallRating", 0),
        "review_count": reviews_data.get("totalReviewCount", 0),
        "item_id": product_data["usItemId"],
        "brand": product_data.get("brand", ""),
        "availability": product_data["availabilityStatus"],
        "type": product_data.get("type", ""),
        "zip_code": product_data["location"].get("postalCode", ""),
        
    }
    
    if(initial_data["seoItemMetaData"]!= None):
        if(initial_data["seoItemMetaData"]["breadCrumbs"] != None):
            i = 1
            for category in initial_data["seoItemMetaData"]["breadCrumbs"]:
                product_info["dep/cat/shelf" + str(i)] = category["name"]
                i += 1

    
    #set default to "not found" in case there is no serving info
    if(nutrition_data["nutritionFacts"]["servingInfo"] != None):
        if(nutrition_data["nutritionFacts"]["servingInfo"]["values"] != None):
            print("found serving info")
            for serving_info in nutrition_data["nutritionFacts"]["servingInfo"]["values"]:
                product_info[serving_info["name"]] = serving_info["value"]
    else:
        product_info["serving_information"] = "not found"
        
    #set default to "not found" in case there is no calories
    if(nutrition_data["nutritionFacts"]["calorieInfo"] != None):
        print("found calorie info")
        product_info["calories"] = nutrition_data["nutritionFacts"]["calorieInfo"]["mainNutrient"]["amount"]
    else:
        product_info["calories"] = "not found"
       

    # #set default to "not found" in case there are no main nutrients
    if(nutrition_data["nutritionFacts"]["keyNutrients"] != None):
        print("found key nutrients")
        values = nutrition_data["nutritionFacts"]["keyNutrients"]["values"]
        for key_nutr_val in values:
            if(key_nutr_val["mainNutrient"] != None):
                key_nutr_name = key_nutr_val["mainNutrient"].get("name", "")
                product_info[key_nutr_name + "_amount"] = key_nutr_val["mainNutrient"].get("amount", "0")
                product_info[key_nutr_name + "_dvp"] = key_nutr_val["mainNutrient"].get("dvp", "0")
                if(key_nutr_val["childNutrients"] != None):
                    for child_nutr_val in key_nutr_val["childNutrients"]:
                        child_nutr_name = child_nutr_val.get("name", "")
                        product_info[child_nutr_name + "_amount"] = child_nutr_val.get("amount", "0")
                        product_info[child_nutr_name + "_dvp"] = child_nutr_val.get("dvp", "0")
    else:
        product_info["key_nutrients"] = "not found"
        
    #set default to "not found" in case there are no vitamins
    if(nutrition_data["nutritionFacts"]["vitaminMinerals"] != None):
        print("found vitamins")
        vitamins = nutrition_data["nutritionFacts"]["vitaminMinerals"]["childNutrients"]
        for vitamin in vitamins:
            # product_info["vitamin_name_"+str(vit_val_count)] = vitamin.get("name", "")
            vit_name = vitamin.get("name", "")
            product_info[vit_name + "_amount"] = vitamin.get("amount", "0")
            product_info[vit_name + "_dvp"] = vitamin.get("dvp", "0")
    else:
        product_info["vitamin_minerals"] = "not found"
        
    
    if(nutrition_data["ingredients"] != None):
        if(nutrition_data["ingredients"]["ingredients"] != None):
            print("found ingredients")
            product_info["ingredients"] = nutrition_data["ingredients"]["ingredients"].get("value", "")
    else:
        product_info["ingredients"] = "not found"
        
    if(product_data["imageInfo"] != None):
        product_info["thumbnail_image_url"] = product_data["imageInfo"]["thumbnailUrl"]
        i = 1
        for image in product_data["imageInfo"]["allImages"]:
            product_info["image_url_" + str(i)] = image["url"]
            i += 1
           
    print("next product")
    
    return product_info


#idealy add ability to query multiple items at once, use set and links set to check if links are being repeated, or fix the issue in data cleaning 

def main():
    print("in main")
    OUTPUT_FILE = "product_info.jsonl"
    CACHE_FILE = "scraped_cache.jsonl" 

    if os.path.exists(CACHE_FILE):
        cache = {}
        with open(CACHE_FILE, 'r') as file:
            for line in file:
                item = json.loads(line)
                cache[item['product_URL']] = item
        print("cache loaded")
    else:
        cache = {}
        print("cache created")
        

    with open(OUTPUT_FILE, 'w') as file:
        
        
        while search_queries:
            current_query = search_queries.pop(0)
            print("\n\nCURRENT QUERY", current_query, "\n\n")
            page_number = 1 
            
            while True:
                links = link_scrape.get_product_links_from_search_page(current_query, page_number)
                if not links or page_number > 24:
                    break

                for link in links:
                    if link not in seen_urls:
                        product_queue.put(link)
                        seen_urls.add(link)
                    
                while not product_queue.empty():
                    product_url = product_queue.get()
                    try:
                        product_info = extract_product_info(product_url, cache)
                        if product_info:
                            file.write(json.dumps(product_info)+"\n")
                    except Exception as e:
                        print(f"Failed to process URL {product_url}. Error {e}")

                page_number += 1
                print(f"Search page {page_number}")
                
        return 0


if __name__ == "__main__":
    main()