from ninja_extra import NinjaExtraAPI
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import NinjaJWTDefaultController

# from store.controllers import ProductsController, StoreController

api = NinjaExtraAPI(auth=JWTAuth())
api.register_controllers(NinjaJWTDefaultController)
# api.add_router("/store", "store.api.router")
# api.add_router("/sales", "sales.api.router")
api.register_controllers(
    "store.controllers.ProductsController",
    "store.controllers.StoreController",
    "store.controllers.CategoryController",
)


@api.get("/status")
def hello(request):
    return { "status": "ok" }
