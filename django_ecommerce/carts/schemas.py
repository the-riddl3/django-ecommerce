from pydantic import BaseModel, PositiveInt, constr

class UpdateCartSchema(BaseModel):
    product_id: PositiveInt
    quantity: PositiveInt

class DeleteCartSchema(BaseModel):
    product_id: PositiveInt