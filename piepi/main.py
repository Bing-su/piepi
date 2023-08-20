from ninja import NinjaAPI

from .upload import router as upload_router

api = NinjaAPI()
api.add_router("", upload_router)
