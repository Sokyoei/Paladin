from django.urls import path
from ninja import NinjaAPI

from .api import ss_router
from .views import index

api = NinjaAPI()

api.add_router("/swallowedstar", ss_router)

urlpatterns = [path('', api.urls), path('index/', index, name='index')]
