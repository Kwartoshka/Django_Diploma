from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Product, ProductReview


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ProductSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True,)

    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    author_id = UserSerializer(read_only=True, )

    class Meta:
        model = ProductReview
        fields = '__all__'

    def create(self, validated_data):

        validated_data['author_id'] = self.context['request'].user

        return super().create(validated_data)

    def validate(self, data):
        method = self.context["request"].method
        user = self.context["request"].user
        product = data['product']
        if method == 'POST':
            marks = [i for i in range(1, 6)]
            if ProductReview.objects.all().filter(author_id=user, product=product):
                raise serializers.ValidationError('Отзыв к данному товару от текущего пользователя уже существует')
            if data['mark'] not in marks:
                raise serializers.ValidationError('Оценка должна быть целым числом от 1 до 5')

        return data