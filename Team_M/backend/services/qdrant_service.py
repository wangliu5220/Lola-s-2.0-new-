from Team_M.backend.db_ingest import client as qdrant_client, embedding_model
from Team_M.backend.models.qdrant_models import ProductRequest
import os
from dotenv import load_dotenv
import boto3
import json
import statistics
from enum import Enum

LIMIT = 20

# Load .env credentials
load_dotenv()

aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")

# # ✅ Use a normal triple-quoted string, not a set
# agent_prompt = """
# Given some Walmart products, you have 2 tasks:

# 1. Search the web and fill in all missing nutritional data for fields that say 'not found'. 
# 2. Rank all the products from least healthy to most healthy, and return your result in the same JSON format as the products you were given.
# """

# helpers 

class HarmNutrient(Enum):
    FAT = "total_fat_DV"
    SUGAR = "included_added_sugars_DV"
    SODIUM = "sodium_DV"

def extract_numeric_part(text: str) -> float:
    """
    Extracts the numeric part of a string field for easy computations
    Args: text_field - a field from an item in the Qdrant database 
    Returns: float
    """
    numeric_str = ""
    is_active = False 
    for char in text: 
        if char == "(":
            is_active = True
        elif is_active and char.isalpha():
            return float(numeric_str)
        else: 
            if is_active:
                numeric_str += char

def get_serving_size(item):
    """
    Gets the serving size of the item in ml/g 
    args: item - an item in our Qdrant database 
    returns: int 
    """
    try: 
        serving_size = item["Nutrition_facts"]["serving_size"]
        final_value = extract_numeric_part(serving_size)
        return final_value
    except KeyError as e: 
        print(f"{e}: Missing important field")
        return None

def get_nutrient_dv(item, nutrient: HarmNutrient) -> float:
    """
    Gets the specified nutrient daily value for a given item
    args: an item from the database 
    returns: the daily value as a float 
    """
    nutrient_str = ""
    try:
        for char in str(item["Nutrition_facts"][nutrient.value]):
            if char.isdigit():
                nutrient_str += char
        try:
            nutrient_float = float(nutrient_str)
        except ValueError as e:
            print(f"Unable to retrieve daily value for {nutrient.value} due to error: {e}.")
            print(item['product_name'])
            return None
        return nutrient_float
    except KeyError as e:
        print(f"{e}: Missing important field")
        return None

class QdrantService:
    def query_and_recommend(self, request: ProductRequest):
        print(f"Received query request: {request}")

        # Generate embedding
        embeddings_gen = embedding_model.embed([request.name + " " + request.description])
        vectorized_query = list(embeddings_gen)

        # Query Qdrant
        search_result = qdrant_client.query_points(
            collection_name="walmart_collection",
            query=vectorized_query[0],
            with_payload=True,
            limit=LIMIT
        ).points

        payloads = [point.payload for point in search_result]

        # Create a list of tuples (item, score)
        composite_rankings = []
        for item in payloads:
            fat = get_nutrient_dv(item, HarmNutrient.FAT)
            sodium = get_nutrient_dv(item, HarmNutrient.SODIUM)
            sugar =  get_nutrient_dv(item, HarmNutrient.SUGAR)
            serving_size = get_serving_size(item)

            if None not in (fat, sodium, sugar, serving_size):
                # Only include the item in the recommendations if we can validate its data to avoid potential misrepresentation
                composite_rankings.append((item, sum((fat, sodium, sugar))/3, item['price']/serving_size)) # format: item, score, price/g

        composite_rankings = sorted(composite_rankings, key=lambda x: x[1])
        upper_quartile = LIMIT//4 if LIMIT >= 4 else 1
        final_results = sorted(composite_rankings[:upper_quartile], key=lambda x: x[2])

        return { "best_match": final_results[0][0], "additional_matches": final_results[1:] if len(final_results) >= 2 else None } if final_results else { "best_match": None, "additional_matches": None }

        