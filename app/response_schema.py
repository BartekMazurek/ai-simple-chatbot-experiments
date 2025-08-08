from pydantic import BaseModel

class CreateEmbeddingResponse(BaseModel):
    status: str
    id: int

class SearchEmbedding(BaseModel):
    id: int
    content: str
    distance: float

class SearchEmbeddingResponse(BaseModel):
    query: str
    data: list[SearchEmbedding]

class CheckEmbeddingResponse(BaseModel):
    query: str
    norm: float

class LlmSearchEmbedding(BaseModel):
    id: int
    content: str
    distance: float

class LlmSearchEmbeddingResponse(BaseModel):
    query: str
    data: list[LlmSearchEmbedding]
    answer: str
