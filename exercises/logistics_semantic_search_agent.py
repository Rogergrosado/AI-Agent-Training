from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    Settings,
    StorageContext,
    load_index_from_storage,
)


from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Exercise 009 — Logistics Semantic Search Agent
# Phase 3: Embeddings and Semantic Retrieval

DATA_DIR = Path("data/exercise_009")
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
STORAGE_DIR = Path("storage/exercise_009")


def load_logistics_documents():
    """Load logistics policy documents using LlamaIndex."""

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {DATA_DIR}")

    reader = SimpleDirectoryReader(
        input_dir=str(DATA_DIR),
        required_exts=[".txt"],
    )

    documents = reader.load_data()

    if not documents:
        raise ValueError("No logistics documents were loaded.")

    return documents


def build_semantic_index(documents):
    """Create or load a vector index using local Hugging Face embeddings."""

    print("\nLoading embedding model...")

    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL)

    Settings.embed_model = embed_model

    if STORAGE_DIR.exists() and any(STORAGE_DIR.iterdir()):
        print("Loading existing vector index...")

        storage_context = StorageContext.from_defaults(persist_dir=str(STORAGE_DIR))

        index = load_index_from_storage(storage_context)

    else:
        print("Building new vector index...")

        index = VectorStoreIndex.from_documents(documents)

        index.storage_context.persist(persist_dir=str(STORAGE_DIR))

        print("Vector index saved successfully.")

    return index


def search_logistics_policies(index, question):
    """Retrieve the most relevant policy documents."""

    retriever = index.as_retriever(similarity_top_k=3)

    results = retriever.retrieve(question)

    print(f"\nQuestion: {question}")
    print("-" * 55)

    for rank, result in enumerate(results, start=1):
        filename = result.node.metadata.get("file_name", "Unknown")

        print(f"\nResult {rank}")
        print(f"Policy: {filename}")
        print(f"Similarity score: {result.score:.4f}")
        print(f"Excerpt: {result.node.text[:200].strip()}...")


def main():
    print("=" * 55)
    print("EXERCISE 009 — LOGISTICS SEMANTIC SEARCH AGENT")
    print("=" * 55)

    documents = load_logistics_documents()
    print(f"\nDocuments loaded: {len(documents)}")

    index = build_semantic_index(documents)
    print("\nVector index created successfully.")

    test_questions = [
        ("A customer received a broken package. " "What policy should we follow?"),
        (
            "A shipment has not arrived by the expected "
            "delivery date. What should the team do?"
        ),
        (
            "A critical shipment exception requires "
            "supervisor review. What is the escalation procedure?"
        ),
    ]

    for test_number, question in enumerate(test_questions, start=1):
        print(f"\n{'=' * 55}")
        print(f"SEMANTIC SEARCH TEST {test_number}")
        print("=" * 55)

        search_logistics_policies(index, question)


if __name__ == "__main__":
    main()
