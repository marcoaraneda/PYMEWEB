from rest_framework import serializers
from .models import Order, OrderItem
from apps.catalogo.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )
    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'quantity',
            'price'
        ]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'store',
            'name',
            'email',
            'phone',
            'address',
            'status',
            'tracking_code',
            'total',
            'created_at',
            'items',
        ]
        read_only_fields = ['tracking_code', 'created_at']

    def validate(self, data):
        store = data.get('store')
        items = data.get('items', [])

        for item in items:
            product = item['product']
            if product.store != store:
                raise serializers.ValidationError(
                    f"El producto {product.id} no pertenece a esta tienda"
                )

        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item in items_data:
            OrderItem.objects.create(order=order, **item)

        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'status',
            'tracking_code',
            'name',
            'email',
            'phone',
            'address',
            'total',
            'created_at',
            'items'
        ]
