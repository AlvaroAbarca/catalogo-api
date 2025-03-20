from asgiref.sync import sync_to_async
from django.http import HttpRequest, HttpResponse
from ninja import ModelSchema, Schema
from ninja_extra import ControllerBase, api_controller, route
from ninja_jwt.authentication import AsyncJWTAuth

from store.models import Category


class CategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ["user"]

class CreateCategorySchema(ModelSchema):
    class Meta:
        model = Category
        fields = "__all__"
        exclude = ["user", "created_at", "updated_at"]


class ResponseListCategorySchema(Schema):
    results: list[CategorySchema]
    count: int


@api_controller("/category", tags=["Category"], auth=AsyncJWTAuth())
class CategoryController(ControllerBase):
    model = Category

    @route.get("/", response=ResponseListCategorySchema)
    async def get_categories(self, request: HttpRequest) -> dict:
        user = self.context.request.user
        categories = await sync_to_async(list)(Category.objects.filter(user=user))
        if categories:
            return {"results": categories, "count": len(categories)}
        return {"results": [], "count": 0}

    @route.get("/{category_id}/", response=CategorySchema)
    async def get_category(self, request: HttpRequest, category_id: int) -> dict:
        try:
            category = await Category.objects.aget(id=category_id)
            return category
        except Category.DoesNotExist:
            return HttpResponse({}, status=404)

    @route.post("/", response=CategorySchema)
    async def create_category(self, request: HttpRequest, category: CreateCategorySchema):
        category = await Category.objects.acreate(**category.dict(), user=request.user)
        return category

    @route.put("/{category_id}/", response=CategorySchema)
    async def update_category(self, request: HttpRequest, category_id: int, category: CreateCategorySchema):
        try:
            category = await Category.objects.aget(id=category_id)
            for key, value in category.dict().items():
                setattr(category, key, value)
            await category.save()
            return category
        except Category.DoesNotExist:
            return HttpResponse({}, status=404)
