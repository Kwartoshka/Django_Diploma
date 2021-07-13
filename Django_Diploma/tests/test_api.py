import json

import pytest
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, \
    HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient
from MyShop.models import Product, ProductReview, Collection, Order, Position
from datetime import date


# @pytest.mark.parametrize(
#     ['include', "price", 'price__gt', 'price__lt', "expected_status", 'length'],
#     (
#             ('', '', '', '', HTTP_200_OK, 3),
#             ("new", '', '', '', HTTP_200_OK, 2),
#             ('pew', '', '', 90000, HTTP_200_OK, 0),
#             ("Samsung", '', '', '', HTTP_200_OK, 1),
#             ('', '', 101000, '', HTTP_200_OK, 0),
#             ('', '', 14000, '', HTTP_200_OK, 2),
#             ('', '', '', 90000, HTTP_200_OK, 2),
#             ('', '', '', 2000, HTTP_200_OK, 0),
#             ('', '', 14000, 90000, HTTP_200_OK, 1),
#             ("iphone", '', '', '', HTTP_200_OK, 1),
#             ('', 100000, '', '', HTTP_200_OK, 1),
#
#     )
# )
# @pytest.mark.django_db
# def test_get_products(include, price, price__gt, price__lt, expected_status, length):
#     client = APIClient()
#     url = reverse("products-list")
#
#     product = Product.objects.bulk_create(
#         [
#             Product(name='iphone', price=100000, description='brand new'),
#             Product(name='Samsung', price=83000, description='new too'),
#             Product(name='nokia', price=13000, description='old')
#         ]
#     )
#     params = {
#         'include': include,
#         'price': price,
#         'price__lt': price__lt,
#         'price__gt': price__gt
#     }
#     resp = client.get(url, params)
#     assert resp.status_code == expected_status
#     print(resp.json())
#     assert len(resp.json()) == length
#
#
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
#     ['author_field', 'author_exists', "creation_date", 'product', 'expected_status', 'length'],
#     (
#             (True, True, '', '', HTTP_200_OK, 3),
#             (True, False, '', '', HTTP_400_BAD_REQUEST, 1),
#             (False, False, date.today(), '', HTTP_200_OK, 6),
#             (False, False, '2020-11-12', '', HTTP_200_OK, 0),
#             (False, False, '', 1, HTTP_200_OK, 3),
#             (False, False, '', 3, HTTP_200_OK, 1),
#     )
# )
# @pytest.mark.django_db
# def test_get_reviews(author_field, author_exists, creation_date, product, expected_status, length):
#     client = APIClient()
#     url = reverse("reviews-list")
#
#     product_1 = Product.objects.create(name='iphone', price=100000, description='brand new')
#     product_2 = Product.objects.create(name='Samsung', price=83000, description='new too')
#     product_3 = Product.objects.create(name='nokia', price=13000, description='old')
#     user_1 = User.objects.create_superuser('stranger1', 'stranger1@stranger.com', 'stranger1')
#     user_2 = User.objects.create_superuser('stranger2', 'stranger2@stranger.com', 'stranger2')
#     user_3 = User.objects.create_superuser('stranger3', 'stranger3@stranger.com', 'stranger3')
#
#     if product == 1:
#         product = product_1.id
#     elif product == 2:
#         product = product_2.id
#     elif product == 3:
#         product = product_3.id
#
#     review = ProductReview.objects.bulk_create(
#         [
#             ProductReview(author=user_1, mark=3, product=product_1),
#             ProductReview(author=user_2, mark=3, product=product_1),
#             ProductReview(author=user_3, mark=3, product=product_1),
#             ProductReview(author=user_1, mark=3, product=product_2),
#             ProductReview(author=user_2, mark=3, product=product_2),
#             ProductReview(author=user_1, mark=3, product=product_3),
#         ]
#     )
#     params = {
#         'author': '',
#         'creation_date': creation_date,
#         'product': product,
#     }
#     if author_field:
#         if author_exists:
#             params['author'] = user_1.id
#         else:
#             params['author'] = user_1.id+999
#
#     resp = client.get(url, params)
#     assert resp.status_code == expected_status
#     assert len(resp.json()) == length
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'product_exists', 'review_exists', 'mark', "expected_status"],
#     (
#             (True, True, False, 5, HTTP_201_CREATED),
#             (True, True, False, 0, HTTP_400_BAD_REQUEST),
#             (True, True, False, -8, HTTP_400_BAD_REQUEST),
#             (True, True, False, 8, HTTP_400_BAD_REQUEST),
#             (True, False, False, 5, HTTP_400_BAD_REQUEST),
#             (True, True, True, 3, HTTP_400_BAD_REQUEST),
#             (False, True, True, 1, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_post_review(authorized, product_exists, review_exists, mark, expected_status):
#     client = APIClient()
#     url = reverse("reviews-list")
#
#     if product_exists:
#         product = Product.objects.create(name="iphone", price=100000)
#     else:
#         product = Product(name="not_iphone", price=100000)
#         product.id = 999
#     review_data = {'mark': mark, 'product': product.id}
#     if authorized:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#         if review_exists:
#             ProductReview.objects.create(mark=1, product=product, author=user)
#
#     resp = client.post(url, review_data)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'review_exists', 'product_exists', 'user_is_creator', 'user_is_admin', 'mark', 'expected_status'],
#     (
#             (True, True, True, True, False, 5, HTTP_200_OK),
#             (True, True, True, True, False, 0, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, 9, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, -7, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 5, HTTP_200_OK),
#             (True, True, True, False, True, 0, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 9, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, -7, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, False, 5, HTTP_403_FORBIDDEN),
#             (True, False, True, True, False, 3, HTTP_404_NOT_FOUND),
#             (True, True, False, True, False, 3, HTTP_400_BAD_REQUEST),
#             (False, True, True, True, False, 5, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_put_review(authorized, review_exists, product_exists, user_is_creator, user_is_admin, mark, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     product_id = product.id
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#     if review_exists:
#         review = ProductReview.objects.create(mark=3, product=product, author=user)
#         review_id = review.id
#
#     else:
#         review_id = 777
#     if not product_exists:
#         product_id = 999
#     if not user_is_creator:
#         if user_is_admin:
#             user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#         else:
#             user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#     url = reverse("reviews-list") + str(review_id) + '/'
#     review_data = {'mark': mark, 'product': product_id}
#     if authorized:
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.put(url, review_data)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'review_exists', 'user_is_creator', 'user_is_admin', 'mark', 'expected_status'],
#     (
#             (True, True, True, False, 5, HTTP_200_OK),
#             (True, True, True, False, 0, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, 9, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, -7, HTTP_400_BAD_REQUEST),
#             (True, True, False, True, 5, HTTP_200_OK),
#             (True, True, False, True, 0, HTTP_400_BAD_REQUEST),
#             (True, True, False, True, 9, HTTP_400_BAD_REQUEST),
#             (True, True, False, True, -7, HTTP_400_BAD_REQUEST),
#             (True, True, False, False, 5, HTTP_403_FORBIDDEN),
#             (True, False, True, False, 3, HTTP_404_NOT_FOUND),
#             (False, True, True, False, 5, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_patch_review(authorized, review_exists, user_is_creator, user_is_admin, mark, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#     if review_exists:
#         review = ProductReview.objects.create(mark=3, product=product, author=user)
#         review_id = review.id
#     else:
#         review_id = 777
#     if not user_is_creator:
#         if user_is_admin:
#             user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#         else:
#             user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#     url = reverse("reviews-list") + str(review_id) + '/'
#     review_data = {'mark': mark}
#     if authorized:
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.patch(url, review_data)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'review_exists', 'user_is_creator', 'user_is_admin', 'expected_status'],
#     (
#             (True, True, True, False, HTTP_204_NO_CONTENT),
#             (True, True, False, True, HTTP_204_NO_CONTENT),
#             (True, True, False, False, HTTP_403_FORBIDDEN),
#             (True, False, True, False, HTTP_404_NOT_FOUND),
#             (False, True, True, False, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_delete_review(authorized, review_exists, user_is_creator, user_is_admin, expected_status):
#     client = APIClient()
#     product = Product.objects.create(name="iphone", price=100000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#     if review_exists:
#         review = ProductReview.objects.create(mark=3, product=product, author=user)
#         review_id = review.id
#     else:
#         review_id = 777
#     if not user_is_creator:
#         if user_is_admin:
#             user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#         else:
#             user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#     url = reverse("reviews-list") + str(review_id) + '/'
#     if authorized:
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.delete(url)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'is_admin', 'product_exists', "expected_status"],
#     (
#             (True, True, True, HTTP_201_CREATED),
#             (True, True, False, HTTP_400_BAD_REQUEST),
#             (True, False, True, HTTP_403_FORBIDDEN),
#             (False, True, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_post_collection(authorized, is_admin, product_exists, expected_status):
#     client = APIClient()
#     url = reverse("collections-list")
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#
#     if product_exists:
#         product_3 = Product.objects.create(name="nokia", price=13000)
#         product_3_id = product_3.id
#     else:
#         product_3_id = 9999
#     collection = {'title': "TEST", 'products': [product_1.id, product_2.id, product_3_id]}
#     if is_admin:
#         user = User.objects.create_superuser('john', 'lennono@thebeatles.com', 'johnpassword')
#     else:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#     if authorized:
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.post(url, collection)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'collection_exists', 'product_exists', 'is_admin', 'expected_status'],
#     (
#             (True, True, True, True, HTTP_200_OK),
#             (True, True, True, False, HTTP_403_FORBIDDEN),
#             (True, True, False, True, HTTP_400_BAD_REQUEST),
#             (True, False, True, True, HTTP_404_NOT_FOUND),
#             (False, True, True, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_put_collection(authorized, collection_exists, product_exists, is_admin, expected_status):
#     client = APIClient()
#
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     if collection_exists:
#         collection = Collection.objects.create(title='First_name')
#         collection.products.set([product_1.id, product_2.id])
#         collection_id = collection.id
#     else:
#         collection_id = 999
#     url = reverse("collections-list") + str(collection_id) + '/'
#     if product_exists:
#         product_3 = Product.objects.create(name="nokia", price=13000)
#         product_3_id = product_3.id
#     else:
#         product_3_id = 9999
#     collection = {'title': "TEST", 'products': [product_1.id, product_2.id, product_3_id]}
#     if is_admin:
#         user = User.objects.create_superuser('john', 'lennono@thebeatles.com', 'johnpassword')
#     else:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#     if authorized:
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.put(url, collection)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'collection_exists', 'product_exists', 'is_admin', 'expected_status'],
#     (
#             (True, True, True, True, HTTP_200_OK),
#             (True, True, True, False, HTTP_403_FORBIDDEN),
#             (True, True, False, True, HTTP_400_BAD_REQUEST),
#             (True, False, True, True, HTTP_404_NOT_FOUND),
#             (False, True, True, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_patch_collection(authorized, collection_exists, product_exists, is_admin, expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     if collection_exists:
#         collection = Collection.objects.create(title='First_name')
#         collection.products.set([product_1.id, product_2.id])
#         collection_id = collection.id
#     else:
#         collection_id = 999
#     url = reverse("collections-list") + str(collection_id) + '/'
#     if product_exists:
#         product_3 = Product.objects.create(name="nokia", price=13000)
#         product_3_id = product_3.id
#     else:
#         product_3_id = 9999
#     collection = {'products': [product_1.id, product_2.id, product_3_id]}
#     if is_admin:
#         user = User.objects.create_superuser('john', 'lennono@thebeatles.com', 'johnpassword')
#     else:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#     if authorized:
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.patch(url, collection)
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'collection_exists', 'is_admin', 'expected_status'],
#     (
#             (True, True, True, HTTP_204_NO_CONTENT),
#             (True, True, False, HTTP_403_FORBIDDEN),
#             (True, False, True, HTTP_404_NOT_FOUND),
#             (False, True, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_delete_collection(authorized, collection_exists, is_admin, expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     if collection_exists:
#         collection = Collection.objects.create(title='First_name')
#         collection.products.set([product_1.id, product_2.id])
#         collection_id = collection.id
#     else:
#         collection_id = 999
#     url = reverse("collections-list") + str(collection_id) + '/'
#     if is_admin:
#         user = User.objects.create_superuser('john', 'lennono@thebeatles.com', 'johnpassword')
#     else:
#         user = User.objects.create_user('john', 'lennono@thebeatles.com', 'johnpassword')
#     if authorized:
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.delete(url)
#     assert resp.status_code == expected_status
#
#
@pytest.mark.parametrize(
    ['authorized', 'is_admin', 'status', 'order_sum', 'order_sum__lt', 'order_sum__gt', 'created_at', 'created_before', 'created_after',
     'updated_at', 'updated_before', 'updated_after', 'product', 'expected_status', 'length'],
    (
            (False, True, '', '', '', '', '', '', '', '', '', '', '', HTTP_401_UNAUTHORIZED, None),
            (True, False, '', '', '', '', '', '', '', '', '', '', '', HTTP_200_OK, 3),
            (True, True, '', '', '', '', '', '', '', '', '', '', '', HTTP_200_OK, 4),

            (True, True, 'NEW', '', '', '', '', '', '', '', '', '', '', HTTP_200_OK, 3),
            (True, True, 'DONE', '', '', '', '', '', '', '', '', '', '', HTTP_200_OK, 1),

            (True, True, '', 100000, '', '', '', '', '', '', '', '', '', HTTP_200_OK, 1),
            (True, True, '', 1000000, '', '', '', '', '', '', '', '', '', HTTP_200_OK, 0),

            (True, True, '', '', 99000, '', '', '', '', '', '', '', '', HTTP_200_OK, 0),
            (True, True, '', '', 120000, '', '', '', '', '', '', '', '', HTTP_200_OK, 1),

            (True, True, '', '', '', 101000, '', '', '', '', '', '', '', HTTP_200_OK, 3),
            (True, True, '', '', '', 990000, '', '', '', '', '', '', '', HTTP_200_OK, 0),

            (True, True, '', '', '', '', date.today(), '', '', '', '', '', '', HTTP_200_OK, 4),
            (True, True, '', '', '', '', '1971-12-12', '', '', '', '', '', '', HTTP_200_OK, 0),

            (True, True, '', '', '', '', '', '1971-12-12', '', '', '', '', '', HTTP_200_OK, 0),
            (True, True, '', '', '', '', '', '2035-12-12', '', '', '', '', '', HTTP_200_OK, 4),

            (True, True, '', '', '', '', '', '', '2035-12-12', '', '', '', '', HTTP_200_OK, 0),
            (True, True, '', '', '', '', '', '', '1971-12-12', '', '', '', '', HTTP_200_OK, 4),

            (True, True, '', '', '', '', '', '', '', date.today(), '', '', '', HTTP_200_OK, 1),
            (True, True, '', '', '', '', '', '', '', '1971-12-12', '', '', '', HTTP_200_OK, 0),

            (True, True, '', '', '', '', '', '', '', '', '1971-12-12', '', '', HTTP_200_OK, 0),
            (True, True, '', '', '', '', '', '', '', '', '2035-12-12', '', '', HTTP_200_OK, 4),

            (True, True, '', '', '', '', '', '', '', '', '', '2035-12-12', '', HTTP_200_OK, 0),
            (True, True, '', '', '', '', '', '', '', '', '', '1971-12-12', '', HTTP_200_OK, 4),

            (True, True, '', '', '', '', '', '', '', '', '', '', 2, HTTP_200_OK, 3)

    )
)
@pytest.mark.django_db
def test_get_orders(authorized, is_admin, status, order_sum, order_sum__lt, order_sum__gt, created_at, created_before, created_after, updated_at, updated_before, updated_after, product, expected_status, length):
    client = APIClient()
    url = reverse("orders-list")

    product_1 = Product.objects.create(name="iphone", price=100000)
    product_2 = Product.objects.create(name="samsung", price=99000)
    product_3 = Product.objects.create(name="nokia", price=13000)

    user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
    user_token = Token.objects.create(user=user)
    superuser = User.objects.create_superuser('admin', 'admin@thebeatles.com', 'admin')
    superuser_token = Token.objects.create(user=superuser)

    position_1 = Position.objects.create(product=product_1, number=1)
    position_2 = Position.objects.create(product=product_2, number=2)
    order = Order.objects.create(author=user, order_sum=298000)
    order.positions.set([position_1.id, position_2.id])

    position_3 = Position.objects.create(product=product_2, number=3)
    position_4 = Position.objects.create(product=product_3, number=4)
    order = Order.objects.create(author=user, order_sum=349000)
    order.positions.set([position_3.id, position_4.id])

    position_5 = Position.objects.create(product=product_2, number=1)
    order = Order.objects.create(author=user, order_sum=100000)
    order.positions.set([position_5.id])

    position_6 = Position.objects.create(product=product_3, number=5)
    position_7 = Position.objects.create(product=product_1, number=8)
    order = Order.objects.create(author=superuser, order_sum=865000)
    order.positions.set([position_6.id, position_7.id])
    #
    # patch_data = {'status': 'DONE'}
    Order.objects.all().filter(id=order.id).update(status='DONE', updating_date=date.today())

    params = {
        'status': status,
        'order_sum': order_sum,
        'order_sum__lt': order_sum__lt,
        'order_sum__gt': order_sum__gt,
        'created_at': created_at,
        'created_before': created_before,
        'created_after': created_after,
        'updated_at': updated_at,
        'updated_before': updated_before,
        'updated_after': updated_after
    }
    if product:
        params['product'] = product_2.id
    if authorized:
        if is_admin:
            client.credentials(HTTP_AUTHORIZATION=f'Token {superuser_token}')
        else:
            client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')

    resp = client.get(url, params)
    assert resp.status_code == expected_status
    if resp.status_code != HTTP_401_UNAUTHORIZED:
        assert len(resp.json()) == length




















# @pytest.mark.parametrize(
#     ['authorized', 'product_exists', 'number', 'expected_status'],
#     (
#             (True, True, 11, HTTP_201_CREATED),
#             (True, True, -9, HTTP_400_BAD_REQUEST),
#             (True, True, 0, HTTP_400_BAD_REQUEST),
#             (True, True, 'five', HTTP_400_BAD_REQUEST),
#             (True, True, 9999, HTTP_400_BAD_REQUEST),
#             (True, False, 11, HTTP_400_BAD_REQUEST),
#             (False, True, 11, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_post_order(authorized, product_exists, number, expected_status):
#     client = APIClient()
#     url = reverse('orders-list')
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     data = {
#         "positions":
#             [
#                 {
#                     "product": product_1.id,
#                     "number": number,
#                 },
#                 {
#                     "product": product_2.id,
#                     "number": number
#                 }
#             ]
#             }
#     if not product_exists:
#         data["positions"].append(
#             {
#                 "product": 999,
#                 "number": 13
#             }
#         )
#     if authorized:
#         user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
#         user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#     resp = client.post(url, data=data, format='json')
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'order_exists', 'product_exists', 'user_is_creator', 'user_is_admin', 'number', 'has_order_status',
#      'expected_status'],
#     (
#             (True, True, True, True, False, 99, False, HTTP_200_OK),
#             (True, True, True, True, False, 99, True, HTTP_403_FORBIDDEN),
#             (True, True, True, True, False, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 99, False, HTTP_200_OK),
#             (True, True, True, False, True, 99, True, HTTP_200_OK),
#             (True, True, True, False, True, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, False, 5, False, HTTP_403_FORBIDDEN),
#             (True, False, True, True, False, 3, False, HTTP_404_NOT_FOUND),
#             (True, True, False, True, False, 3, False, HTTP_400_BAD_REQUEST),
#             (False, True, True, True, False, 5, False, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_put_order(authorized, order_exists, product_exists, user_is_creator, user_is_admin, number, has_order_status,
#                    expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#
#     if order_exists:
#         position_1 = Position.objects.create(product=product_1, number=3)
#         position_2 = Position.objects.create(product=product_2, number=7)
#         order = Order.objects.create(author=user)
#         order.positions.set([position_1.id, position_2.id])
#         order_id = order.id
#     else:
#         order_id = 777
#
#     if authorized:
#         if not user_is_creator:
#             if user_is_admin:
#                 user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#             else:
#                 user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#
#     url = reverse("orders-list") + str(order_id) + '/'
#     new_data = {
#         "positions":
#             [
#                 {
#                     "product": product_1.id,
#                     "number": number,
#                 },
#
#             ]
#     }
#     if not product_exists:
#         product_3_id = 999
#         new_data["positions"].append(
#             {
#                 "product": product_3_id,
#                 "number": 11
#             }
#         )
#     if has_order_status:
#         new_data['status'] = 'DONE'
#     resp = client.put(url, json.dumps(new_data), content_type="application/json")
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'order_exists', 'product_exists', 'user_is_creator', 'user_is_admin', 'number', 'has_order_status',
#      'expected_status'],
#     (
#             (True, True, True, True, False, 99, False, HTTP_200_OK),
#             (True, True, True, True, False, 99, True, HTTP_403_FORBIDDEN),
#             (True, True, True, True, False, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 99, False, HTTP_200_OK),
#             (True, True, True, False, True, 99, True, HTTP_200_OK),
#             (True, True, True, False, True, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, False, 5, False, HTTP_403_FORBIDDEN),
#             (True, False, True, True, False, 3, False, HTTP_404_NOT_FOUND),
#             (True, True, False, True, False, 3, False, HTTP_400_BAD_REQUEST),
#             (False, True, True, True, False, 5, False, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_patch_order(authorized, order_exists, product_exists, user_is_creator, user_is_admin, number,
#                      has_order_status, expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#
#     if order_exists:
#         position_1 = Position.objects.create(product=product_1, number=3)
#         position_2 = Position.objects.create(product=product_2, number=7)
#         order = Order.objects.create(author=user)
#         order.positions.set([position_1.id, position_2.id])
#         order_id = order.id
#     else:
#         order_id = 777
#
#     if authorized:
#         if not user_is_creator:
#             if user_is_admin:
#                 user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#             else:
#                 user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#
#     url = reverse("orders-list") + str(order_id) + '/'
#     new_data = {
#         "positions":
#             [
#                 {
#                     "product": product_1.id,
#                     "number": number,
#                 },
#
#             ]
#     }
#     if not product_exists:
#         product_3_id = 999
#         new_data["positions"].append(
#             {
#                 "product": product_3_id,
#                 "number": 11
#             }
#         )
#     if has_order_status:
#         new_data['status'] = 'DONE'
#     resp = client.patch(url, json.dumps(new_data), content_type="application/json")
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'order_exists', 'product_exists', 'user_is_creator', 'user_is_admin', 'number', 'has_order_status',
#      'expected_status'],
#     (
#             (True, True, True, True, False, 99, False, HTTP_200_OK),
#             (True, True, True, True, False, 99, True, HTTP_403_FORBIDDEN),
#             (True, True, True, True, False, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, True, False, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 99, False, HTTP_200_OK),
#             (True, True, True, False, True, 99, True, HTTP_200_OK),
#             (True, True, True, False, True, 0, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, 999, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, True, -7, False, HTTP_400_BAD_REQUEST),
#             (True, True, True, False, False, 5, False, HTTP_403_FORBIDDEN),
#             (True, False, True, True, False, 3, False, HTTP_404_NOT_FOUND),
#             (True, True, False, True, False, 3, False, HTTP_400_BAD_REQUEST),
#             (False, True, True, True, False, 5, False, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_patch_order(authorized, order_exists, product_exists, user_is_creator, user_is_admin, number, has_order_status,
#                      expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#
#     if order_exists:
#         position_1 = Position.objects.create(product=product_1, number=3)
#         position_2 = Position.objects.create(product=product_2, number=7)
#         order = Order.objects.create(author=user)
#         order.positions.set([position_1.id, position_2.id])
#         order_id = order.id
#     else:
#         order_id = 777
#
#     if authorized:
#         if not user_is_creator:
#             if user_is_admin:
#                 user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#             else:
#                 user = User.objects.create_user('stranger', 'stranger@stranger.com', 'stranger')
#                 user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#
#     url = reverse("orders-list") + str(order_id) + '/'
#     new_data = {
#         "positions":
#             [
#                 {
#                     "product": product_1.id,
#                     "number": number,
#                 },
#
#             ]
#     }
#     if not product_exists:
#         product_3_id = 999
#         new_data["positions"].append(
#             {
#                 "product": product_3_id,
#                 "number": 11
#             }
#         )
#     if has_order_status:
#         new_data['status'] = 'DONE'
#     resp = client.patch(url, json.dumps(new_data), content_type="application/json")
#     assert resp.status_code == expected_status
#
#
# @pytest.mark.parametrize(
#     ['authorized', 'order_exists', 'is_admin', 'expected_status'],
#     (
#             (True, True, True, HTTP_204_NO_CONTENT),
#             (True, True, False, HTTP_403_FORBIDDEN),
#             (True, False, True, HTTP_404_NOT_FOUND),
#             (False, True, True, HTTP_401_UNAUTHORIZED),
#     )
# )
# @pytest.mark.django_db
# def test_delete_order(authorized, order_exists, is_admin, expected_status):
#     client = APIClient()
#     product_1 = Product.objects.create(name="iphone", price=100000)
#     product_2 = Product.objects.create(name="samsung", price=99000)
#     user = User.objects.create_user('johnathan', 'lennono@thebeatles.com', 'johnpassword')
#     user_token = Token.objects.create(user=user)
#
#     if order_exists:
#         position_1 = Position.objects.create(product=product_1, number=3)
#         position_2 = Position.objects.create(product=product_2, number=7)
#         order = Order.objects.create(author=user)
#         order.positions.set([position_1.id, position_2.id])
#         order_id = order.id
#     else:
#         order_id = 777
#
#     if authorized:
#         if is_admin:
#             user = User.objects.create_superuser('stranger', 'stranger@stranger.com', 'stranger')
#             user_token = Token.objects.create(user=user)
#         client.credentials(HTTP_AUTHORIZATION=f'Token {user_token}')
#
#     url = reverse("orders-list") + str(order_id) + '/'
#     resp = client.delete(url)
#     assert resp.status_code == expected_status
