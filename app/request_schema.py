from pydantic import BaseModel

class CreateEmbeddingRequest(BaseModel):
    text: str
