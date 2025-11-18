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
    FAT = "total_fat_absolute"
    SUGAR = "total_sugars_absolute"
    SODIUM = "sodium_absolute"


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
        return 0

def get_nutrient_per_hundred(item, nutrient: HarmNutrient) -> float:
    """
    Gets the fat per 100/ml/g
    args: item 
    """
    nutrient_str = ""
    try:
        for char in str(item["Nutrition_facts"][nutrient.value]):
            if char.isdigit():
                nutrient_str += char
        try:
            nutrient_float = float(nutrient_str)
        except ValueError as e:
            return None
        serving_size = get_serving_size(item)
        if serving_size and serving_size > 0:
            return nutrient_float/serving_size
        else:
            return None

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
        composite_ranking = []
        fat_rankings = []
        sodium_rankings = []
        sugar_rankings = []
        for item in payloads:
            # calculate harm score using Kaela's algorithm 
            # use regex to get the grams/serving if food, ml/serving if beverage 
            # get fat/100g/ml 
            fat = get_nutrient_per_hundred(item, HarmNutrient.FAT)
            sodium = get_nutrient_per_hundred(item, HarmNutrient.SODIUM)
            sugar =  get_nutrient_per_hundred(item, HarmNutrient.SUGAR)
            if None not in (fat, sodium, sugar):
                fat_rankings.append((item, fat))
                sodium_rankings.append((item, sodium))
                sugar_rankings.append((item, sugar))

        fat_rankings = sorted(fat_rankings, key=lambda x: x[1])
        sodium_rankings = sorted(sodium_rankings, key=lambda x: x[1])
        sugar_rankings = sorted(sugar_rankings, key=lambda x: x[1])
        
        rankings: dict[str: list] = {}
        for tup in fat_rankings:
            rankings[tup[0]["product_name"]] = [tup[0], fat_rankings.index(tup)]
        for tup in sodium_rankings:
            rankings[tup[0]["product_name"]][1] += sodium_rankings.index(tup)
        for tup in sugar_rankings:
            rankings[tup[0]["product_name"]][1] =  (rankings[tup[0]["product_name"]][1] + sugar_rankings.index(tup)) / 3
        

        composite_ranking = sorted([rankings[key] for key in rankings], key=lambda x: x[1])
        final_results = sorted(composite_ranking[:5], key=lambda x: x[0]['price']/get_serving_size(x[0]))

        print(final_results[0])
        return { "best_match": final_results[0][0], "additional_matches": final_results[1:] }

        