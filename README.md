# Simple AI chatbot based on FastAPI & Postgres (RAG)

***

### 1 - How to run

> docker compose up -d

***

### 2 - Fill the database with embeddings

**Endpoint:** `POST /create/embedding`  
**Content-Type:** `application/json`

**Body:**
```json
{
  "text": "Some text ..."
}
```
**Response:**
```json
{
  "status": "success",
  "id": 1
}
```

***

### 3 - Request the most accurate embeddings
**Endpoint:** `POST /search`  
**Content-Type:** `application/json`

**Body:**
```json
{
  "query": "Some text ..."
}
```
**Response:**
```json
{
  "query": "Some text ...",
  "data": [
    {
      "id": 1,
      "content": "Some text ...",
      "distance": 0.0
    }
  ]
}
```

***

### 4 - Ask the LLM for an answer
**Endpoint:** `POST /llm/search`  
**Content-Type:** `application/json`

**Body:**
```json
{
  "query": "Some text ..."
}
```
**Response:**
```json
{
  "query": "Some text ...",
  "data": [
    {
      "id": 1,
      "content": "Some text ...",
      "distance": 0.0
    }
  ],
  "answer": "..."
}
```
