from pydantic import BaseModel


class Product(BaseModel):
    id: str
    title: str
    description: str
    category: str
    description_vector: list[float] | None = None
