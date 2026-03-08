from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: int
    message: str
