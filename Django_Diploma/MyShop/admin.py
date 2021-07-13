from django.contrib import admin
from .models import Product, ProductReview, Collection, Order, Position


class CollectionInline(admin.TabularInline):
    model = Collection.products.through


class OrderInline(admin.TabularInline):
    model = Order.positions.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('updating_date',)
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # model = Order.positions.through

    inlines = [OrderInline]
    exclude = ['positions', 'updating_date', 'order_sum']
    # list_filter = ('order_sum',)
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    # inlines = [PositionInline]
    pass


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    inlines = [CollectionInline]
    exclude = ['products', 'updating_date']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    exclude = ['updating_date']
    pass
