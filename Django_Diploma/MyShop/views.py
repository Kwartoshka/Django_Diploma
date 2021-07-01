from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductReview, Collection, Order
from .serializers import ProductSerializer, ProductReviewSerializer, CollectionSerializer, OrderSerializer,\
    OrderPositionsIdSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from datetime import date


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        # print(dir(request).parser_context())
        return True


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser(), IsAuthor()]
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
            return [IsAuthenticated()]
        elif self.action == 'update':

            data = self.request.data
            print(data)
            _mutable = data._mutable
            data._mutable = True
            data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAuthor()]
        return []


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

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


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # def get_serializer_class(self):
    #     if self.action in {'list', 'retrieve'}:
    #         return OrderSerializer
    #     else:
    #         return OrderPositionsIdSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser()]

        elif self.action == 'update':

            data = self.request.data
            print(data)
            # _mutable = data._mutable
            # data._mutable = True
            data['updating_date'] = date.today()
            print(data)

            return [IsAuthenticated(), IsAdminUser()]

        return []

