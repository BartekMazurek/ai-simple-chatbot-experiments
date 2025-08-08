from pydantic import BaseModel

class CreateEmbeddingRequest(BaseModel):
    text: str

class SearchEmbeddingRequest(BaseModel):
    query: str

class CheckEmbeddingRequest(BaseModel):
    query: str

class LlmSearchEmbeddingRequest(BaseModel):
    query: str
