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
