from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from ninja import ModelSchema, Router, Schema
from ninja_jwt.authentication import AsyncJWTAuth

from store.models import Store

router = Router(tags=["Store"])


class StoreSchema(ModelSchema):
    class Meta:
        model = Store
        fields = "__all__"
        exclude = ["user"]

class StoreCreateSchema(ModelSchema):
    class Meta:
        model = Store
        fields = "__all__"
        exclude = ["user", "created_at", "updated_at"]


class ResponseListSchema(Schema):
    results: list[StoreSchema]
    count: int


@router.get("/store", response=ResponseListSchema, auth=AsyncJWTAuth())
async def get_stores(request: HttpRequest) -> HttpResponse:
    stores = await sync_to_async(list)(Store.objects.all())
    return {"results": stores, "count": len(stores)}


@router.get("/store/{store_id}", response=StoreSchema, auth=AsyncJWTAuth())
async def get_store(request: HttpRequest, store_id: int) -> HttpResponse:
    store = await Store.objects.aget(id=store_id)
    return store

@router.post("/store", response=StoreSchema, auth=AsyncJWTAuth())
async def create_store(request: HttpRequest, store: StoreCreateSchema) -> HttpResponse:
    store = await Store.objects.acreate(**store.dict(), user=request.user)
    return store


@router.put("/store/{store_id}", response=StoreSchema, auth=AsyncJWTAuth())
async def update_store(request: HttpRequest, store_id: int, store: StoreCreateSchema) -> HttpResponse:
    store = await Store.objects.aget(id=store_id)
    for key, value in store.dict().items():
        if key in store.dict(exclude={"user"}):
            setattr(store, key, value)
    await store.save()
    return store
