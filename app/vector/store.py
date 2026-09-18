# step 12. Insert chunks into vector store
import psycopg

from app.vector.embeddings import embed


def get_connection():
    return psycopg.connect(
        "host=localhost "
        "port=5432 "
        "dbname=rag "
        "user=postgres "
        "password=postgres"
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