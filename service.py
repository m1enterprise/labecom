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
    return {"message": "service.py API"}

# GET
@app.get("/products", response_model=list[Product])
def get_products():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, name, price FROM products LIMIT 10"))
            rows = [dict(row._mapping) for row in result]
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET by id
@app.get("/products/{id}", response_model=Product)
def get_product_by_id(id: int):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, name, price FROM products WHERE id = :id"),
                {"id": id}
            )
            row = result.fetchone()

            if row is None:
                raise HTTPException(status_code=404, detail="Product not found")

            product = dict(row._mapping)

        return product

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST
# @app.post("/products", response_model=Product)
# def create_product(product: Product = Body(..., example={"name": "T-Shirt", "price": 25.0})):
#     try:
#         with engine.connect() as conn:
#             # If ID is auto-generated, don't insert it
#             result = conn.execute(
#                 text(
#                     "INSERT INTO products (name, price) "
#                     "VALUES (:name, :price) "
#                     "RETURNING id, name, price"
#                 ),
#                 {"name": product.name, "price": product.price}
#             )
#             # Fetch the inserted row
#             inserted_row = result.fetchone()
#             if inserted_row is None:
#                 raise HTTPException(status_code=500, detail="Failed to insert product")
#             new_product = dict(inserted_row._mapping)
#         return new_product
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
