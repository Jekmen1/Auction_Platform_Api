from rest_framework import serializers
from .models import User, Product, Bid
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True,
                                         'style': {'input_type': 'password'}}}
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class ProductSerializer(serializers.ModelSerializer):
    current_highest_bidder = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'min_bid', 'start_time', 'last_bid_time', 'current_highest_bid', 'current_highest_bidder']

class BidSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'user', 'product', 'amount', 'timestamp']