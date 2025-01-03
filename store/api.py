from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from ninja import ModelSchema, Router, Schema

from store.models import Store

router = Router(tags=['Store'])

class StoreSchema(ModelSchema):
    class Meta:
        model = Store
        fields = "__all__"
        exclue = ['user']

class ResponseListSchema(Schema):
    results: list[StoreSchema]
    count: int

@router.get("/stores", response=ResponseListSchema)
async def get_stores(request: HttpRequest) -> HttpResponse:
    stores = await sync_to_async(list)(Store.objects.all())
    return stores
