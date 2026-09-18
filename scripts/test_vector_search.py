from app.vector.store import search


results = search(
    "How does Kubernetes run containers on a node?"
)

for result in results:
    print("Score:", result["score"])
    print("Chunk:", result["chunk_id"])
    print(result["text"][:300])
    print("-" * 80)