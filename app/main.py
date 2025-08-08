from fastapi import FastAPI, HTTPException
from db import connection
from pgvector.psycopg2 import register_vector
from psycopg2.extras import RealDictCursor
from sentence_transformer import model
from transformer import tokenizer, llm
import numpy as np

from request_schema import CreateEmbeddingRequest
from response_schema import CreateEmbeddingResponse
from request_schema import SearchEmbeddingRequest
from response_schema import SearchEmbedding
from response_schema import SearchEmbeddingResponse
from request_schema import CheckEmbeddingRequest
from response_schema import CheckEmbeddingResponse
from request_schema import LlmSearchEmbeddingRequest
from response_schema import LlmSearchEmbedding
from response_schema import LlmSearchEmbeddingResponse

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

@app.post("/llm/search", response_model=LlmSearchEmbeddingResponse)
def search_embedding_llm(request: LlmSearchEmbeddingRequest):
    try:
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
            LlmSearchEmbedding(
                id=row["id"],
                content=row["content"],
                distance=row["distance"],
            )
            for row in results
        ]

        cur.close()
        conn.close()

        # PREPARE LLM PROMPT
        combined_context = " ".join([row["content"] for row in results])
        prompt = (
            f"Answer the following question based only on the provided context.\n\n"
            f"Context:\n{combined_context}\n\n"
            f"Question:\n{request.query}\n\n"
            f"Answer:"
        )

        # TOKENIZATION AND LLM INFERENCE
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        outputs = llm.generate(**inputs, max_length=150, num_beams=5)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

        #print(f"Prompt: {prompt}")
        #print(f"Generated answer: {answer}")

        return LlmSearchEmbeddingResponse(query=request.query, answer=answer, data=data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-normalization", response_model=CheckEmbeddingResponse)
def check_normalization(request: CheckEmbeddingRequest):
    try:
        #embedding = model.encode(request.query).tolist()
        embedding = model.encode(request.query, normalize_embeddings=True).tolist()
        norm = np.linalg.norm(embedding)

        return {"query": request.query, "norm": norm}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
