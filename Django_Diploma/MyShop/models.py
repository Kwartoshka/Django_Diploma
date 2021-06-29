from django.db import models
from django.conf import settings


class StatusChoices(models.TextChoices):
    NEW = 'NEW', 'Новый'
    IN_PROGRESS = 'IN_PROGRESS', 'В процессе'
    DONE = 'DONE', 'Выполнен'


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(default='')
    price = models.IntegerField(default=0)
    creation_date = models.DateField(
        auto_now_add=True
    )
    updating_date = models.DateField(null=True)

    def __str__(self):
        return f'{self.name} - {self.price} рублей'


class ProductReview(models.Model):
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(default='')
    mark = models.IntegerField()
    creation_date = models.DateField(
        auto_now_add=True
    )
    updating_date = models.DateField(null=True)


class Order(models.Model):
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # positions =
    status = models.TextField(default=StatusChoices.NEW, choices=StatusChoices.choices)
    order_sum = models.IntegerField()
    creation_date = models.DateField(
        auto_now_add=True
    )
    updating_date = models.DateField(null=True)


class Collection(models.Model):

    title = models.CharField(max_length=128)
    text = models.TextField(default='')
    products = models.ManyToManyField(Product)
    creation_date = models.DateField(
        auto_now_add=True
    )
    updating_date = models.DateField(null=True)

