from pydantic import BaseModel



class StockRequest(BaseModel):
    quantity: int

class InventoryCreatSchema(BaseModel):
    name: str
    description: str
    stock: int
    price: float
