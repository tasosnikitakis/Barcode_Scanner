from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def product_by_barcode(request, barcode):
    try:
        print(f"Fetching product with barcode: {barcode}")
        product = Product.objects.get(barcode=barcode)
        serializer = ProductSerializer(product)
        print(f"Product found: {serializer.data}")
        return Response(serializer.data)
    except Product.DoesNotExist:
        print(f"Product with barcode {barcode} not found")
        return Response({'error': 'Product not found'}, status=404)
    except Exception as e:
        print(f"Unexpected error: {e}")
        return Response({'error': 'Internal Server Error', 'details': str(e)}, status=500)


