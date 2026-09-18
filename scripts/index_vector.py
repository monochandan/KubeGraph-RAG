# Step 12.1 Create ingestion script:

from app.ingestion.chunker import load_documents
from app.vector.store import insert_chunk, get_connection
from app.vector.embeddings import embed

documents = load_documents()

print(f"Found {len(documents)} chunks")

for i, document in enumerate(documents):

    insert_chunk(document)

    print(
        f"{i + 1}/{len(documents)}"
    )

