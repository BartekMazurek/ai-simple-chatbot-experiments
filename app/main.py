from fastapi import FastAPI, HTTPException
from db import connection
from pgvector.psycopg2 import register_vector
from psycopg2.extras import RealDictCursor
from transformer import model

from request_schema import CreateEmbeddingRequest
from response_schema import CreateEmbeddingResponse
from request_schema import SearchEmbeddingRequest
from response_schema import SearchEmbedding
from response_schema import SearchEmbeddingResponse

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/create/embedding", response_model=CreateEmbeddingResponse)
def create_embedding(request: CreateEmbeddingRequest):
    try:
        embedding = model.encode(request.text, normalize_embeddings=True).tolist()

        conn = connection()
        register_vector(conn)
        cur = conn.cursor()

        insert_query = """
            INSERT INTO vector.items (content, embedding)
            VALUES (%s, %s)
            RETURNING id;
        """

        cur.execute(insert_query, (request.text, embedding))
        id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success", "id": id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search", response_model=SearchEmbeddingResponse)
def search_embedding(request: SearchEmbeddingRequest):
    try:

        # SEMANTIC SEARCH EXAMPLE
        embedding = model.encode(request.query, normalize_embeddings=True).tolist()

        conn = connection()
        register_vector(conn)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        sql = """
            SELECT id, content, embedding <-> %s::VECTOR AS distance
            FROM vector.items
            ORDER BY distance
            LIMIT %s;
        """

        cur.execute(sql, (embedding, 5))
        results = cur.fetchall()

        data = [
            SearchEmbedding(
                id=row["id"],
                content=row["content"],
                distance=row["distance"],
            )
            for row in results
        ]

        cur.close()
        conn.close()

        return SearchEmbeddingResponse(query=request.query, data=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
