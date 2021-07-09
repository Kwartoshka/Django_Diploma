import pytest
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.reverse import reverse

from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
from rest_framework.urls import urlpatterns
# from MyShop.models import Product

from MyShop.models import Product, ProductReview


# @pytest.mark.parametrize(
#     ['authorized', 'superuser', "name", "price", "expected_status"],
#     (
#             (True, True, "iphone", 100000, HTTP_201_CREATED),
#             (True, True, "iphone 11", 100000, HTTP_201_CREATED),
#             (True, True, "-100", -100, HTTP_400_BAD_REQUEST),
#             (True, True, "ывыфыфв", 0, HTTP_201_CREATED),
#             (True, False, "iphone", 100000, HTTP_403_FORBIDDEN),
#             (False, True, "iphone", 100000, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_post_product(authorized, superuser, name, price, expected_status):
#     client = APIClient()
#     if authorized:
#         if superuser:
#             user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
#         else:
#             user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     url = reverse("products-list")
#     product = {"name": name, "price": price}
#     resp = client.post(url, product)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'superuser', "name", "price", "expected_status"],
#     (
#             (True, True, "iphone", 200000, HTTP_200_OK),
#             (True, True, "-iphone", -100, HTTP_400_BAD_REQUEST),
#             (True, True, 12, 100000, HTTP_200_OK),
#             (True, True, "ывыфыфв", 0, HTTP_200_OK),
#             (True, False, "iphone", 100000, HTTP_403_FORBIDDEN),
#             (False, True, "iphone", 100000, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_put_product(authorized, superuser, name, price, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     if authorized:
#         if superuser:
#             user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
#         else:
#             user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     url = reverse("products-list") + str(product.id) + '/'
#     product = {"name": name, "price": price}
#     resp = client.put(url, product)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'superuser', "price", "expected_status"],
#     (
#             (True, True, 200000, HTTP_200_OK),
#             (True, True, -100, HTTP_400_BAD_REQUEST),
#             (True, True, 100000, HTTP_200_OK),
#             (True, True, 0, HTTP_200_OK),
#             (True, False, 100000, HTTP_403_FORBIDDEN),
#             (False, True, 100000, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_patch_product(authorized, superuser, price, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     if authorized:
#         if superuser:
#             user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
#         else:
#             user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     url = reverse("products-list") + str(product.id) + '/'
#     product = {"price": price}
#     resp = client.patch(url, product)
#     assert resp.status_code == expected_status
#
# @pytest.mark.parametrize(
#     ['authorized', 'superuser', "expected_status"],
#     (
#             (True, True, HTTP_204_NO_CONTENT),
#             (True, False, HTTP_403_FORBIDDEN),
#             (False, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_delete_product(authorized, superuser, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     if authorized:
#         if superuser:
#             user = User.objects.create_superuser('john', 'lennon@thebeatles.com', 'johnpassword')
#         else:
#             user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     url = reverse("products-list") + str(product.id) + '/'
#     resp = client.delete(url)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'exists', 'mark', "expected_status"],
#     (
#             (True, False, 5, HTTP_201_CREATED),
#             (True, False, 0, HTTP_400_BAD_REQUEST),
#             (True, False, -8, HTTP_400_BAD_REQUEST),
#             (True, False, 8, HTTP_400_BAD_REQUEST),
#             (True, True, 3, HTTP_400_BAD_REQUEST),
#             (False, True, 1, HTTP_401_UNAUTHORIZED),
#
#     )
# )
# @pytest.mark.django_db
# def test_post_review(authorized, exists, mark, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     url = reverse("reviews-list")
#     review_data = {'mark': mark, 'product': product.id}
#     if authorized:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#         if exists:
#             review = ProductReview.objects.create(mark=1, product=product, author=user)
#
#     resp = client.post(url, review_data)
#     assert resp.status_code == expected_status

@pytest.mark.parametrize(
    ['authorized', 'exists', 'mark', "expected_status"],
    (
            (True, True, 5, HTTP_200_OK),
            (True, True, 0, HTTP_400_BAD_REQUEST),
            (True, True, -8, HTTP_400_BAD_REQUEST),
            (True, True, 8, HTTP_400_BAD_REQUEST),
            (True, False, 3, HTTP_404_NOT_FOUND),
            (False, False, 1, HTTP_401_UNAUTHORIZED),

    )
)
@pytest.mark.django_db
def test_put_review(authorized, exists, mark, expected_status):
    client = APIClient()
    product = Product.objects.create(name="iphone", price=100000)
    product_id = 999
    superuser = User.objects.create_superuser('johnathan', 'lennono@thebeatles.com', 'johnpassword')
    superuser_token = Token.objects.create(user=superuser)
    if exists:
        review = ProductReview.objects.create(mark=3, product=product, author=superuser)
        product_id = product.id
    url = reverse("reviews-list") + str(review.id) + '/'

    review_data = {'mark': mark, 'product': product_id}
    if authorized:
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user_token = Token.objects.create(user=user)
        client.credentials(HTTP_AUTHORIZATION=f'Token {superuser_token}')
    resp = client.put(url, review_data)
    print(resp.json())
    assert resp.status_code == expected_status
