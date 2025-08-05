from pydantic import BaseModel

class CreateEmbeddingResponse(BaseModel):
    status: str
    id: int
