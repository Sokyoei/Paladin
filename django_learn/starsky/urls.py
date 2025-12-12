from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BlackHoleViewSet, ConstellationViewSet, GalaxyViewSet, NebulaViewSet, StarViewSet, index

router = DefaultRouter()
router.register(r'stars', StarViewSet)
router.register(r'galaxies', GalaxyViewSet)
router.register(r'constellations', ConstellationViewSet)
router.register(r'black-holes', BlackHoleViewSet)
router.register(r'nebulae', NebulaViewSet)

urlpatterns = [path("index/", index, name="index"), path('starsky/', include(router.urls))]
