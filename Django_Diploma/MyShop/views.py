from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductReview, Collection, Order, Order2, OrderPosition2
from .serializers import ProductSerializer, ProductReviewSerializer, CollectionSerializer, OrderSerializer,\
     Order2Serializer, OrderPosition2Serializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from datetime import date
from .filters import ProductFilter, ProductReviewFilter, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend


class IsAuthor(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        # print(dir(request).parser_context())
        return True


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductReviewFilter

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'update':

            data = self.request.data
            # print(data)
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
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
            # print(data)
            # _mutable = data._mutable
            # data._mutable = True
            data['updating_date'] = date.today()
            # print(data)

            return [IsAuthenticated(), IsAdminUser()]

        return []


class Order2ViewSet(ModelViewSet):
    queryset = Order2.objects.all()
    serializer_class = Order2Serializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = Order2Filter

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser()]

        elif self.action == 'update':

            data = self.request.data

            data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAdminUser()]

        return []


class OrderPosition2ViewSet(ModelViewSet):
    queryset = OrderPosition2.objects.all()
    serializer_class = OrderPosition2Serializer