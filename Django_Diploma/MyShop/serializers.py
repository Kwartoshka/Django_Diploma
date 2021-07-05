from django.contrib.auth.models import User
from rest_framework import serializers, permissions
from rest_framework.utils import model_meta
from .models import Product, ProductReview, Collection, Order, Position, OrderPosition2, OrderPosition


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
        # print(validated_data)
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
        positions = validated_data['positions']
        positionz = []
        order_sum = 0
        for position in positions:
            product = position['product']
            price = product.price
            number = position['number']
            order_sum += price * number
            instance = Position.objects.create(product=product, number=number)
            positionz.append(instance.id)
        author = validated_data['author']
        instance = Order.objects.create(author=author, order_sum=order_sum)
        for position in positionz:
            OrderPosition.objects.create(order_id=instance.id, position_id=position)

        return instance

    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        m2m_fields = []

        for attr, value in validated_data.items():

            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        for attr, value in m2m_fields:
            if attr != 'positions':

                # print(attr)
                # print(value)

                field = getattr(instance, attr)
                # print(field)
                field.set(value)
            else:
                # print(attr)
                # print(value)
                obj = Order.objects.get(id=instance.id)

                positions = Position.objects.all().filter(orders=obj)
                # print(positions)
                # products = [p.product for p in positions]
                # print(products)
                relations = []
                new = []
                for p in value:
                    product = p['product']
                    number = p['number']
                    position = positions.filter(product=product)
                    if position:
                        if position[0].number != number:
                            uppa = Position.objects.filter(product=product)
                            object = Position.objects.filter(product=product)[0]
                            uppa.update(number=number)
                        relations.append(product)
                    else:
                        new_position = Position.objects.create(product=product, number=number)
                        new.append(new_position)
                # print(positions)
                print(relations)
                if relations:
                    for position in positions:

                        if position.product not in relations:
                            print('ЕГО ТУТ НЕТ')
                            Position.objects.filter(id=position.id).delete()
                for position in new:
                    OrderPosition.objects.create(order_id=instance.id, position_id=position.id)

        instance.save()

        return instance

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


class OrderPosition2Serializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPosition2
        fields = ['id', 'position_id']


class Order2Serializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, )
    positions = OrderPosition2Serializer(many=True,)

    class Meta:
        model = Order
        fields = '__all__'
