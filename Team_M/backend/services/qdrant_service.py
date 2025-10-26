from db_ingest import client, embedding_model

class QdrantService:
    def query(request):
        embeddings_gen = embedding_model.embed([request])
        vectorized_query = list(embeddings_gen)
        search_result = client.query_points(
            collection_name="walmart_collection",
            query=vectorized_query[0],
            with_payload=True,
            limit=5
        ).points

        return search_result