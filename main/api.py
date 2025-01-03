from ninja_extra import NinjaExtraAPI
from ninja_jwt.controller import NinjaJWTDefaultController

# from sales.api import router as sales_router
# from store.api import router as store_router

api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)
api.add_router('/store', 'store.api.router')
api.add_router('/sales', 'sales.api.router')

@api.get("/hello")
def hello(request):
    return "Hello world"
