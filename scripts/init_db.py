# step 10. Create PostgreSQL vector database
import psycopg


# 1. Connect to the default database and create "rag"
# admin = psycopg.connect(
    # "host=localhost port=5432 dbname=postgres user=postgres password=postgres",
    # autocommit=True
# )
# with admin.cursor() as cur:
    # cur.execute("CREATE DATABASE rag")
# admin.commit()
# admin.close()'

# 2.Now connect to "rag" and set up schema
conn = psycopg.connect(
    "host=localhost port=5432 dbname=rag user=postgres password=postgres"
)

with conn.cursor() as cur:

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            chunk_id TEXT PRIMARY KEY,
            document_id TEXT NOT NULL,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            embedding vector(384)
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS chunks_embedding_idx
        ON chunks
        USING hnsw (embedding vector_cosine_ops)
    """)

conn.commit()
conn.close()

print("Database initialized")