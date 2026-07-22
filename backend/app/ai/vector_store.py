"""
Vector Store

Future support for semantic search.
"""


class VectorStore:
    """
    Handles vector storage and similarity search.
    """

    def add_document(
        self,
        document: str,
    ):
        raise NotImplementedError(
            "Vector storage will be implemented in Phase 2."
        )

    def search(
        self,
        query: str,
    ):
        raise NotImplementedError(
            "Semantic search will be implemented in Phase 2."
        )
    