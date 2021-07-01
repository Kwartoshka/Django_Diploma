from django.contrib.auth.models import User
from rest_framework import serializers, permissions
from .models import Product, ProductReview, Collection, Order, Position, OrderPosition


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['name']


class ProductReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, )

    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        print(validated_data)
        return super().create(validated_data)

    def validate(self, data):
        method = self.context["request"].method
        user = self.context["request"].user
        marks = [i for i in range(1, 6)]
        if method == 'POST':
            product = data['product']
            if ProductReview.objects.all().filter(author=user, product=product):
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


class PositionSerializer(serializers.ModelSerializer):
    # product = ProductShortSerializer(read_only=True, )

    class Meta:
        model = Position
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, )
    positions = PositionSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        print(validated_data)
        positions = validated_data['positions']
        print(positions)
        positionz = []
        order_sum = 0
        for position in positions:
            product = position['product']
            price = product.price
            number = position['number']
            order_sum += price * number
            instance = Position.objects.create(product=product, number=number)
            print(instance.id)
            positionz.append(instance.id)
        author = validated_data['author']
        # pos = positions.set()
        instance = Order.objects.create(author=author, order_sum=order_sum)
        for position in positionz:
            OrderPosition.objects.create(order_id=instance.id, position_id=position)

        return instance
        # return super().create(validated_data)


class OrderPositionsIdSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, )
    # positions = PositionSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user

        return super().create(validated_data)



