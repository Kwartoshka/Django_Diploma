from django.contrib import admin
from .models import Product, ProductReview, Collection, Order, Position, Order2


class CollectionInline(admin.TabularInline):
    model = Collection.products.through


class OrderInline(admin.TabularInline):
    model = Order.positions.through


class Order2Inline(admin.TabularInline):
    model = Order2.positions.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # model = Order.positions.through

    inlines = [OrderInline]
    exclude = ['positions', 'updating_date']
    list_filter = ('order_sum',)
    pass


@admin.register(Order2)
class Order2Admin(admin.ModelAdmin):
    inlines = [Order2Inline]
    exclude = ['positions']
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
    exclude = ['updating_date']
    pass
