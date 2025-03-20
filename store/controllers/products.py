from datetime import datetime

from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from ninja import ModelSchema, Schema
from ninja_extra import ControllerBase, api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

from store.models import Category, Product, Store


class ProductSchema(Schema):
    id: int
    name: str
    description: str
    price: float
    image: str | None
    created_at: datetime
    updated_at: datetime

    category_id: int
    store_id: int

# class Meta:
#     model = Product
#     fields = "__all__"
#     exclude = ["image"]

class ProductCreateSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["image", "created_at", "updated_at"]
        fields_optional = ["image"]


class ResponseListProductSchema(Schema):
    results: list[ProductSchema]
    count: int


@api_controller("/products", tags=["Products"], auth=AsyncJWTAuth())
class ProductsController(ControllerBase):
    model = Product

    @route.get("/", response=ResponseListProductSchema)
    async def get_products(self, request: HttpRequest) -> dict:
        stores = await sync_to_async(list)(Store.objects.filter(user=request.user))
        if stores:
            store = stores[0]
            products = await sync_to_async(list)(Product.objects.filter(store=store))
            return {"results": products, "count": len(products)}
        return {"results": [], "count": 0}

    @route.put("/{product_id}/", response=ProductSchema)
    async def update_product(self, request: HttpRequest, product_id: int, product: ProductSchema):
        try:
            product = await Product.objects.aget(id=product_id)
            for key, value in product.dict().items():
                setattr(product, key, value)
            await product.save()
            return product
        except Product.DoesNotExist:
            return HttpResponse({}, status=404)

    @route.post("/", response=ProductSchema)
    async def create_product(self, request: HttpRequest, product: ProductCreateSchema):
        try:
            store = await sync_to_async(Store.objects.get)(user=request.user, id=product.store)
            category = await sync_to_async(Category.objects.get)(user=request.user, id=product.category)
        except (Store.DoesNotExist, Category.DoesNotExist):
            return HttpResponse({"detail": "Tienda o categoría no encontrada."}, status=404)

        product_data = product.dict()
        product_data.pop("store")
        product_data.pop("category")
        new_product = await Product.objects.acreate(**product_data, store=store, category=category)
        return new_product
