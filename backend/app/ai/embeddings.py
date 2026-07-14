"""
Embeddings Service

Future support for semantic search.
"""


class EmbeddingService:
    """
    Handles text embeddings.
    """

    def generate_embedding(
        self,
        text: str,
    ):
        raise NotImplementedError(
            "Embedding generation will be implemented in Phase 2."
        )