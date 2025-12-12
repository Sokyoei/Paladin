from django.urls import path
from ninja import NinjaAPI

from .api import ss_router

api = NinjaAPI()

api.add_router("/swallowedstar", ss_router)

urlpatterns = [path('', api.urls)]
