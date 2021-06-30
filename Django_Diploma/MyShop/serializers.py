from django.contrib.auth.models import User
from rest_framework import serializers, permissions
from .models import Product, ProductReview, Collection, Order, OrderProduct


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ('id', 'product')


class ProductSerializer(serializers.ModelSerializer):
    # creator = UserSerializer(read_only=True,)

    class Meta:
        model = Product
        fields = '__all__'

    # def validate(self, data):
    #     method = self.context['request'].method
    #     if method =='POST':
    #         if data['price'] < 0:
    #             raise serializers.ValidationError('Цена товара не может быть отрицательной')
    #     elif method in {'PUT', 'PATCH'}:
    #         price = data.get('price', None)
    #         if price is None:
    #             pass
    #         elif price < 0:
    #             raise serializers.ValidationError('Цена товара не может быть отрицательной')
    #
    #     return data


class ProductReviewSerializer(serializers.ModelSerializer):
    author_id = UserSerializer(read_only=True, )
    print(author_id)

    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data)
        validated_data['author_id'] = self.context['request'].user

        return super().create(validated_data)

    def validate(self, data):
        print(data)
        method = self.context["request"].method
        user = self.context["request"].user
        marks = [i for i in range(1, 6)]
        if method == 'POST':
            product = data['product']
            if ProductReview.objects.all().filter(author_id=user, product=product):
                raise serializers.ValidationError('Отзыв к данному товару от текущего пользователя уже существует')
            if data['mark'] not in marks:
                raise serializers.ValidationError('Оценка должна быть целым числом от 1 до 5')
        elif method in {'PATCH', 'PUT'}:
            mark = data.get('mark', None)
            if mark not in marks and mark is not None:
                raise serializers.ValidationError('Оценка должна быть целым числом от 1 до 5')

        return data


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = '__all__'


# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    # for position in positions: = OrderProductSerializer(read_only=True, )
    # author = UserSerializer(read_only=True, )
    # print(positions)

    class Meta:
        model = Order
        fields = '__all__'

