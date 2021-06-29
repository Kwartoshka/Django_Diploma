from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductReview
from .serializers import ProductSerializer, ProductReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import date


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action == 'update':
            data = self.request.data
            _mutable = data._mutable
            data._mutable = True
            data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAdminUser()]
        return []


class ProductReviewViewSet(ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action == 'update':
            data = self.request.data
            _mutable = data._mutable
            data._mutable = True
            data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAdminUser()]
        return []