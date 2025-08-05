from fastapi import FastAPI, HTTPException
from db import connection
from transformer import model

from request_schema import CreateEmbeddingRequest
from response_schema import CreateEmbeddingResponse

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "OK"}


@app.post("/create/embedding", response_model=CreateEmbeddingResponse)
def create_embedding(request: CreateEmbeddingRequest):
    try:
        embedding = model.encode(request.text).tolist()
        embedding_str = str(embedding).replace("\n", "")

        conn = connection()
        cur = conn.cursor()

        insert_query = """
            INSERT INTO vector.items (content, embedding)
            VALUES (%s, %s)
            RETURNING id;
        """

        cur.execute(insert_query, (request.text, embedding_str))
        id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success", "id": id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
