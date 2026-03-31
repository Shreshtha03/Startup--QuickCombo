from rest_framework import serializers
from .models import User, Category, MenuItem, Order, OrderItem, Address, Restaurant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'name', 'date_joined']


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'image_url',
                  'is_veg', 'is_available', 'is_featured', 'is_combo_eligible',
                  'rating', 'prep_time', 'category_name', 'category_icon', 'category',
                  'restaurant', 'restaurant_name']


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'slug']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'name', 'price', 'quantity', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'user_name', 'user_phone', 'delivery_address',
                  'delivery_lat', 'delivery_lng', 'status', 'payment_method',
                  'payment_status', 'subtotal', 'delivery_fee', 'total',
                  'notes', 'created_at', 'updated_at', 'rider_lat', 'rider_lng', 'items']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'label', 'line1', 'line2', 'city', 'pincode',
                  'lat', 'lng', 'is_default']
