"""Script to ingest processed JSON Files into Qdrant"""
import json

# initialize the client
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from typing import List
from fastembed import TextEmbedding # default free model, can alternatively use others e.g. OpenAI
from qdrant_client.models import PointStruct
import numpy as np

client = QdrantClient(url="http://localhost:6333")
embedding_model = TextEmbedding()
print("Loaded default model: BAAI/bge-small-en-v1.5")

if not client.collection_exists(collection_name="walmart_collection"):
    client.create_collection(
        collection_name="walmart_collection",
        vectors_config=VectorParams(size=384, distance=Distance.DOT),
    )

# Script with 2 parts: 
def extract_upsert(limit=100):
    payloads: List[str] = [] # docs we will upsert to qdrant 
    """Parse through the entire JSON file, extract key fields and construct a payload, vectorize the payload, and upsert into qdrant"""
# 1. Iterate through all the elements and construct payload - Daniel
    with open("Team_M/Data/beverages/final_response.jsonl", "r") as file:
        for line in file:
            if limit == 0:
                break
            json_obj = json.loads(line)
            payload = {
                'product_name': json_obj.get('product_name', None), 
                'universal_product_code': json_obj.get('universal_product_code', None), 
                'Nutrition_facts': json_obj.get('Nutrition_facts', None),
                'price': json_obj.get('price', None),
                'avg_rating': json_obj.get('avg_rating', None),
                'image_url': json_obj.get('image_url', None),
                'product_URL': json_obj.get('product_URL', None)

            }
            payloads.append(json.dumps(payload))
            limit -= 1
        


# 2. Embed each payload as a vector - Jayden 
# assume payload is instantiated at this step 
    embeddings_generator = embedding_model.embed(documents=[ json.loads(payload)['product_name'] for payload in payloads])
    embeddings_list = list(embeddings_generator)
    len(embeddings_list[0])  
    mapped_items_and_vectors = list(zip(payloads, embeddings_list))
    # print(f"Shape: {mapped_items_and_vectors}")
    # print("Embeddings:\n", mapped_items_and_vectors)

# 3. Upsert items and their corresponding vectors into qdrant 
    operation_info = client.upsert(
        collection_name="walmart_collection",
        wait=True,
        points = [PointStruct(id=i, vector=list(tup[1]), payload=json.loads(tup[0])) for i, tup in enumerate(mapped_items_and_vectors)],
    )

    print(operation_info)




def main():
    extract_upsert()


if __name__ == "__main__":
    main()