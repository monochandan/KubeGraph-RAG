# step 9. Build the document chunker

from pathlib import Path
import hashlib


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        if end == len(words):
            break

        start = end - overlap

    return chunks


def load_documents(directory="data/raw"):
    documents = []

    for path in Path(directory).glob("*.md"):
        text = path.read_text(encoding="utf-8")

        document_id = hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()[:16]

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{path.stem}:chunk_{i}"

            documents.append({
                "document_id": document_id,
                "source": str(path),
                "chunk_id": chunk_id,
                "text": chunk,
            })

    return documents