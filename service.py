from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ecommerce Backend")

# przykład modelu danych
class Product(BaseModel):
    id: int
    name: str
    price: float

# endpoint testowy
@app.get("/")
def read_root():
    return {"status": "ok", "service": "backend"}

# endpoint: lista produktów
@app.get("/products")
def list_products():
    data = [
        Product(id=1, name="Shoes", price=100),
        Product(id=2, name="Hat", price=40)
    ]
    return data

# endpoint: pobranie jednego produktu
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {"id": product_id, "name": "Demo", "price": 50}
