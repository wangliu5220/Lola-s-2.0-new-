from Team_M.backend.db_ingest import client as qdrant_client, embedding_model
from Team_M.backend.models.qdrant_models import ProductRequest
import os
from dotenv import load_dotenv
import boto3
import json
import statistics

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

class QdrantService:
    def query_and_recommend(self, request: ProductRequest):
        print(f"Received query request: {request.content}")

        # Generate embedding
        embeddings_gen = embedding_model.embed([request.content])
        vectorized_query = list(embeddings_gen)

        # Query Qdrant
        search_result = qdrant_client.query_points(
            collection_name="walmart_collection",
            query=vectorized_query[0],
            with_payload=True,
            limit=3
        ).points

        # # Extract product data from Qdrant results
        # products = [point.payload for point in search_result]
        # products_json = json.dumps(products, indent=2)

        # # Initialize Bedrock runtime client (use a distinct name)
        # bedrock_client = boto3.client(
        #     "bedrock-runtime",
        #     region_name=aws_region,
        #     aws_access_key_id=aws_access_key,
        #     aws_secret_access_key=aws_secret_key
        # )

        # model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"

        # # Build Claude message with both the prompt and the data
        # messages = [
        #     {
        #         "role": "user",
        #         "content": [
        #             {"text": f"{agent_prompt}\n\nHere are the products:\n{products_json}"}
        #         ]
        #     }
        # ]

        # response = bedrock_client.converse(
        #     modelId=model_id,
        #     messages=messages
        # )

        # # Extract Claude's actual reply text
        # try:
        #     reply_text = response["output"]["message"]["content"][0]["text"]
        # except (KeyError, IndexError):
        #     reply_text = json.dumps(response, indent=2)  # fallback if structure changes

        # return reply_text

        # generate harm_score
        payloads = [point.payload for point in search_result]

        # Create a list of tuples (item, score)
        scored_items = []
        for item in payloads:
            score = statistics.mean([
                float(item["Nutrition_facts"]["total_fat_DV"].replace('%', '')),
                float(item["Nutrition_facts"]["sodium_DV"].replace('%', '')),
                float(item["Nutrition_facts"]["included_added_sugars_DV"].replace('%', '')),
            ])
            scored_items.append((item, score))

        final_result = sorted(scored_items, key=lambda x: x[1])

        return final_result

        