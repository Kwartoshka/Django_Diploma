# from django.urls import reverse
from django.urls import reverse
from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductReview, Collection, Order
from .serializers import ProductSerializer, ProductReviewSerializer, CollectionSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission, SAFE_METHODS
from datetime import date
from .filters import ProductFilter, ProductReviewFilter, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend


class IsAuthorOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print(obj.author)
        print(request.user)
        return obj.author == request.user or bool(request.user and request.user.is_staff)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
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
        elif self.action in ['update', 'partial_update', 'destroy']:

            data = self.request.data
            _mutable = data._mutable
            data._mutable = True
            data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAuthorOrAdmin()]
        return []


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:

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

    def get_permissions(self):
        print(self.action)
        if self.action == 'create':
            return [IsAuthenticated()]

        elif self.action in ['update', 'partial_update', 'destroy']:

            data = self.request.data
            try:
                data['updating_date'] = date.today()
            except AttributeError:
                _mutable = data._mutable
                data._mutable = True
                data['updating_date'] = date.today()
            status = data.get('status', None)
            if (not [IsAuthenticated(), IsAdminUser()]) and status:
                return False

            return [IsAuthenticated(), IsAuthorOrAdmin()]
        return []
