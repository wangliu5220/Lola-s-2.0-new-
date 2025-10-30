from Team_M.backend.db_ingest import client, embedding_model
from Team_M.backend.models.qdrant_models import ProductRequest

class QdrantService:
    def query(self, request: ProductRequest):
        print(f"Received query request: {request.content}")
        embeddings_gen = embedding_model.embed([request.content])
        vectorized_query = list(embeddings_gen)
        search_result = client.query_points(
            collection_name="walmart_collection",
            query=vectorized_query[0],
            with_payload=True,
            limit=3
        ).points

        return [point.payload for point in search_result]