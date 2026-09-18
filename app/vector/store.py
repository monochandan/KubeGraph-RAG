import psycopg
from app.vector.embeddings import embed

def get_connection():
    return psycopg.connect(
        "host=localhost port=5432 dbname=rag user=postgres password=postgres"
    )


def insert_chunk(chunk):
    embedding = embed(chunk["text"])

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO chunks
            (chunk_id, document_id, source, text, embedding)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id)
            DO UPDATE SET
                text = EXCLUDED.text,
                embedding = EXCLUDED.embedding
            """,
            (
                chunk["chunk_id"],
                chunk["document_id"],
                chunk["source"],
                chunk["text"],
                embedding,
            ),
        )

    conn.commit()
    conn.close()

# step 13. Implement vector search
def search(query: str, k: int = 5):
    query_embedding = embed(query)

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                chunk_id,
                source,
                text,
                1 - (embedding <=> %s::vector) AS score
            FROM chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s
            """,
            (
                query_embedding,
                query_embedding,
                k,
            ),
        )

        results = cur.fetchall()

    conn.close()

    return [
        {
            "chunk_id": row[0],
            "source": row[1],
            "text": row[2],
            "score": float(row[3]),
        }
        for row in results
    ]