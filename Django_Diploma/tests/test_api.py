import pytest
from rest_framework.reverse import reverse

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
from rest_framework.urls import urlpatterns
from MyShop.models import Product


@pytest.mark.django_db
def test_post():
    client = APIClient()

    url = reverse("products-list")
    products = Product.objects.bulk_create(
        [
            Product(name='IPHONE', price=10),
            Product(name='XIAOOOOMU',price=999)
        ]
    )
    header = {"Authorization": 'Token 488d250fb920b853ab5b786c5757bda8db3e6efc'}
    resp = client.post(url, **header)
    print(resp.json())

    assert resp.status_code == HTTP_200_OK

@pytest.mark.django_db
def test_put():
    client = APIClient()
    product = Product.objects.get(name='IPHONE')
    product_id = product.id

    url = reverse("products-list")
    products = Product.objects.bulk_create(
        [
            Product(name='IPHONE', price=10),
            Product(name='XIAOOOOMU',price=999)
        ]
    )
    header = {"Authorization": 'Token 488d250fb920b853ab5b786c5757bda8db3e6efc'}
    resp = client.post(url, **header)
    print(resp.json())

    assert resp.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_product():
    client = APIClient()
    url = reverse("products-list")
    resp = client.get(url)
    print(resp.json)

    assert resp.status_code == HTTP_200_OK
