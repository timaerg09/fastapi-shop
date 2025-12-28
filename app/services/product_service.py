from fastapi import HTTPException
from typing import List

from sqlalchemy.orm import Session

from backend.app.models import Product
from backend.app.repositories.category_repository import CategoryRepository
from backend.app.repositories.product_repository import ProductRepository
from backend.app.schemas.product import ProductResponse, ProductCreate

from ..schemas.product import ProductListResponse


class ProductService:
    def __init__(self, db: Session):
        self.category_repository = CategoryRepository(db)
        self.product_repository = ProductRepository(db)

    def get_all_products(self) -> ProductListResponse:
        products = self.product_repository.get_all()
        products_response = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
        return ProductResponse.model_validate(product)

    def get_products_by_category(self, category_id: int) -> ProductListResponse:
        if not self.category_repository.get_by_id(category_id):
            raise HTTPException(status_code=404, detail=f"Category with id {category_id} not found")

        products = self.product_repository.get_by_category(category_id)
        products_response = [ProductResponse.model_validate(product) for product in products]
        return ProductListResponse(products=products_response, total=len(products_response))

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        if not self.category_repository.get_by_id(product_data.category_id):
            raise HTTPException(status_code=404, detail=f"Category with id {product_data.category_id} not found")

        product = self.product_repository.create(product_data)
        return ProductResponse.model_validate(product)