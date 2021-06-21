from django.contrib import admin
from .models import Product, Order, ProductReview, Collection
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass
