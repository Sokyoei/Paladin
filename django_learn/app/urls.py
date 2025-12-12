from django.urls import path

from .views import index, root, sse_view

urlpatterns = [
    # deafult view
    path('', root, name='root'),  # html root
    # app view
    path('index/', index, name='index'),
    path('sse', sse_view),
]
