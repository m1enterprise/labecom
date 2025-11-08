import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text

app = FastAPI(title="Ecommerce API")

# -------------------------------
# Environment variables
# -------------------------------
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "postgres")
CLOUD_SQL_CONNECTION_NAME = os.environ.get("CLOUD_SQL_CONNECTION_NAME")  # PROJECT:REGION:INSTANCE

# -------------------------------
# Determine connection URL
# -------------------------------
# Production / Cloud Run: connect via Unix socket
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{CLOUD_SQL_CONNECTION_NAME}"

# -------------------------------
# SQLAlchemy engine
# -------------------------------
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# -------------------------------
# Data model
# -------------------------------
class Product(BaseModel):
    id: int
    name: str
    price: float

# -------------------------------
# Routes
# -------------------------------
@app.get("/")
def home():
    return {"message": "Hello from FastAPI + Cloud SQL!", "user": DB_USER, "password": DB_PASS, "name": DB_NAME, "cloud_sql": CLOUD_SQL_CONNECTION_NAME}

@app.get("/products", response_model=list[Product])
def get_products():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, price FROM products LIMIT 10"))
            rows = [dict(row._mapping) for row in result]
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
