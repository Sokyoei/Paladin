from django.urls import path

from .views import index, sse_view

urlpatterns = [
    # deafult view
    path('', index),
    # sse view
    path('sse', sse_view),
]
