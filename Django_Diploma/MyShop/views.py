from rest_framework.viewsets import ModelViewSet
from .models import Product, ProductReview, Collection, Order
from .serializers import ProductSerializer, ProductReviewSerializer, CollectionSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from datetime import date
from .filters import ProductFilter, ProductReviewFilter, OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsStatus, IsAuthorOrAdmin


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
            try:
                data['updating_date'] = date.today()
            except AttributeError:
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
        if self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAuthorOrAdmin()]
        elif self.action in ['update', 'partial_update']:

            data = self.request.data
            try:
                data['updating_date'] = date.today()
            except AttributeError:
                _mutable = data._mutable
                data._mutable = True
                data['updating_date'] = date.today()

            return [IsAuthenticated(), IsAuthorOrAdmin()]
        return []


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
            data = self.request.data
            try:
                data['updating_date'] = date.today()
            except AttributeError:
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

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_staff:
                return self.queryset
            elif self.request.user.is_authenticated and self.request.user:
                return self.queryset.filter(author=self.request.user)
            else:
                return self.queryset
        return self.queryset

    def get_permissions(self):
        print(self.action)
        if self.action in ['retrieve', 'list']:
            return [IsAuthenticated(), IsAuthorOrAdmin()]
        elif self.action == 'create':
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.action in ['update', 'partial_update']:
            data = self.request.data
            try:
                data['updating_date'] = date.today()
            except AttributeError:
                _mutable = data._mutable
                data._mutable = True
                data['updating_date'] = date.today()
            status = data.get('status', None)
            if status:
                return [IsStatus()]

            return [IsAuthenticated(), IsAuthorOrAdmin()]
        return []
