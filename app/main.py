from app.ingestion.chunker import load_documents

docs = load_documents()

print(len(docs))
print(docs[0])