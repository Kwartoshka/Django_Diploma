from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from datetime import date


class StatusChoices(models.TextChoices):

    NEW = 'NEW', 'Новый'
    IN_PROGRESS = 'IN_PROGRESS', 'В процессе'
    DONE = 'DONE', 'Выполнен'


class BaseTable(models.Model):
    creation_date = models.DateField(auto_now_add=True)
    updating_date = models.DateField(null=True, default=None)

    class Meta:
        abstract = True


class Product(BaseTable):

    name = models.CharField(max_length=128)
    description = models.TextField(default='')
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.name} ({self.price} руб.)'


class ProductReview(BaseTable):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(default='')
    mark = models.IntegerField(validators=[
            MaxValueValidator(5),
            MinValueValidator(1)])

    def __str__(self):
        return f'Отзыв {self.author_id} на {self.product}'


class Order(BaseTable):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    positions = models.ManyToManyField('Position', related_name='orders', through='OrderPosition')
    status = models.TextField(default=StatusChoices.NEW, choices=StatusChoices.choices)
    order_sum = models.IntegerField(null=True)

    def __str__(self):
        return f'заказ {self.id} от {self.author} на {self.order_sum} рублей ({self.status})'


class Collection(BaseTable):

    title = models.CharField(max_length=128)
    text = models.TextField(default='')
    products = models.ManyToManyField(Product, related_name='collections')

    def __str__(self):
        return self.title


class Position(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)])

    def __str__(self):
        return f'{self.product} - {self.number} шт.'

    def display(self):
        return self.objects.all()


class OrderPosition(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
