from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
import os

app = FastAPI(title="Ecommerce API")

# Pobieramy zmienne środowiskowe
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "mypassword")
DB_NAME = os.environ.get("DB_NAME", "ecomdb")
DB_HOST = os.environ.get("DB_HOST")  # np. /cloudsql/project:region:instance

# Tworzymy connection string SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Model danych
class Product(BaseModel):
    id: int
    name: str
    price: float

# Routes
@app.get("/")
def home():
    return {"message": "Hello from FastAPI + Cloud SQL!"}

@app.get("/products", response_model=list[Product])
def get_products():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, price FROM products LIMIT 10"))
            rows = [dict(row) for row in result]
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/products", response_model=Product)
def create_product(product: Product):
    try:
        with engine.connect() as conn:
            conn.execute(
                text("INSERT INTO products (id, name, price) VALUES (:id, :name, :price)"),
                {"id": product.id, "name": product.name, "price": product.price}
            )
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
