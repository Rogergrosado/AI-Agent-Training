
# Exercise 009 — Logistics Semantic Search Agent

## Unit 2.2 — LlamaIndex

### Objective

Build a local semantic search system that retrieves relevant logistics policies using natural-language questions.

Unlike traditional keyword matching, semantic retrieval uses vector embeddings to identify documents based on meaning and contextual similarity.

### Technologies

- Python 3.12
- LlamaIndex
- Hugging Face Embeddings
- Sentence Transformers
- Local vector index persistence

### Knowledge Base

The system uses three sample logistics policies:

1. Damaged Shipment Handling (DAM-001)
2. Delayed Delivery Management (DEL-002)
3. Shipment Exception Escalation (ESC-003)

### Architecture

1. Load logistics policy documents from local text files.
2. Generate document embeddings using a local model.
3. Build a vector index with LlamaIndex.
4. Save the index to local storage.
5. Load the existing index on subsequent executions.
6. Retrieve relevant policies for natural-language queries.

### Validation Results

Three test questions were evaluated:

| Test | Scenario | Top Retrieved Policy |
|---|---|---|
| 1 | Broken package | DAM-001 |
| 2 | Missed delivery date | DEL-002 |
| 3 | Critical exception requiring supervisor review | ESC-003 |

All three tests returned the expected policy as the highest-ranked result.

### Index Persistence

The vector index is stored in `storage/exercise_009/`.

The first execution creates and saves the index. Subsequent executions load the existing index, avoiding unnecessary rebuilding.

### Limitations

- The knowledge base contains only three sample policies.
- Similarity scores do not guarantee factual correctness.
- The current implementation retrieves policy excerpts rather than generating complete operational recommendations.
- The persisted index must be rebuilt when source documents change.

### Key Takeaway

Semantic retrieval provides a foundation for building more reliable logistics AI systems by connecting natural-language questions to relevant operational documents.
