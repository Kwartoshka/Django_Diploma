from django.contrib import admin
from .models import Product, ProductReview, Collection, Order, Position
# Register your models here.


class CollectionInline(admin.TabularInline):
    model = Collection.products.through


class OrderInline(admin.TabularInline):
    model = Order.positions.through


# class PositionInline(admin.TabularInline):
#     model = Position.products.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    exclude = ['positions', 'updating_date']
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    # inlines = [PositionInline]
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionInline]
    exclude = ['products']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    pass


