from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
from config import settings
from schemas import Document, SearchResult
import uuid


class NeuralSearchService:
    def __init__(self):
        # Connect to Qdrant
        self.qdrant_client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        # Load embedding model (may take time on first startup)
        self.model = SentenceTransformer(settings.MODEL_NAME)
        self.vector_size = self.model.get_sentence_embedding_dimension()

    def recreate_collection(self):
        """Create collection if it does not exist"""
        collections = self.qdrant_client.get_collections()
        exists = any(c.name == settings.COLLECTION_NAME for c in collections.collections)

        if not exists:
            self.qdrant_client.create_collection(
                collection_name=settings.COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=self.vector_size,
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{settings.COLLECTION_NAME}' created.")

    def upload_documents(self, documents: list[Document]):
        """Vectorize and upload documents"""
        points = []
        for doc in documents:
            # Generate embedding vector
            vector = self.model.encode(doc.text).tolist()

            # Create Qdrant point
            points.append(models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text": doc.text, **doc.metadata}
            ))

        self.qdrant_client.upsert(
            collection_name=settings.COLLECTION_NAME,
            points=points
        )
        return len(points)

    def search(self, query: str, limit: int = 5, filter_key: str = None, filter_value: str = None):
        """Search for similar documents"""
        query_vector = self.model.encode(query).tolist()

        # Optional filtering configuration
        query_filter = None
        if filter_key and filter_value:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key=filter_key,
                        match=models.MatchValue(value=filter_value)
                    )
                ]
            )

        hits = self.qdrant_client.search(
            collection_name=settings.COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            limit=limit
        )

        return [
            SearchResult(
                text=hit.payload["text"],
                metadata={k: v for k, v in hit.payload.items() if k != "text"},
                score=hit.score
            ) for hit in hits
        ]


# Create service singleton
search_service = NeuralSearchService()
