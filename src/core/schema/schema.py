from pydantic import BaseModel

class ResponseBaseSchema(BaseModel):
    success: bool = True
    message: str
