from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from ninja import ModelSchema, Schema
from ninja_extra import ControllerBase, api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

from store.models import Store

# from ninja_extra.permissions import PermissionBase
# permissions=[IsAuthenticated, IsAdmin]
# class IsAdmin(PermissionBase):
#     def has_permission(self, context):
#         return context.request.user.is_staff


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


@api_controller("/store", tags=["Store"], auth=AsyncJWTAuth())
class StoreController(ControllerBase):
    model = Store

    @route.get("/", response=ResponseListSchema)
    async def get_stores(self, request: HttpRequest) -> HttpResponse:
        stores = await sync_to_async(list)(Store.objects.all())
        return {"results": stores, "count": len(stores)}

    @route.get("/{store_id}", response=StoreSchema)
    async def get_store(self, request: HttpRequest, store_id: int) -> HttpResponse:
        try:
            store = await Store.objects.aget(id=store_id)
            return store
        except Store.DoesNotExist:
            return HttpResponse({}, status=404)

    @route.post("/", response=StoreSchema)
    async def create_store(self, request: HttpRequest, store: StoreCreateSchema) -> HttpResponse:
        store = await Store.objects.acreate(**store.dict(), user=request.user)
        return store

    @route.put("/{store_id}", response=StoreSchema)
    async def update_store(self, request: HttpRequest, store_id: int, store: StoreCreateSchema) -> HttpResponse:
        store = await Store.objects.aget(id=store_id)
        for key, value in store.dict().items():
            if key in store.dict(exclude={"user"}):
                setattr(store, key, value)
        await store.save()
        return store
