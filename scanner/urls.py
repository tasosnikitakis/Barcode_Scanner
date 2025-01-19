from django.urls import path
from .views import product_by_barcode, index

urlpatterns = [
    # path('', index, name='index'),
    path('product/<str:barcode>/', product_by_barcode, name='product-by-barcode'),
]
