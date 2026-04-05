from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from .models import User, Order, MenuItem, Restaurant, Category
from .serializers import OrderSerializer, MenuItemSerializer, RestaurantSerializer, CategorySerializer

@api_view(['GET'])
def admin_stats(request):
    # Only staff can see stats
    email = request.headers.get('X-User-Email', '')
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({'error': 'Forbidden'}, status=403)
    except User.DoesNotExist:
        return Response({'error': 'Unauthorized'}, status=401)

    total_sales = Order.objects.filter(status='delivered').aggregate(Sum('total'))['total__sum'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    active_orders = Order.objects.exclude(status__in=['delivered', 'cancelled']).count()
    
    return Response({
        'total_sales': total_sales,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'active_orders': active_orders,
    })

@api_view(['GET', 'PATCH'])
def admin_orders(request):
    email = request.headers.get('X-User-Email', '')
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({'error': 'Forbidden'}, status=403)
    except User.DoesNotExist:
        return Response({'error': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        orders = Order.objects.all().order_by('-created_at')
        return Response(OrderSerializer(orders, many=True).data)
    
    elif request.method == 'PATCH':
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=404)

@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def admin_menu_items(request):
    email = request.headers.get('X-User-Email', '')
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({'error': 'Forbidden'}, status=403)
    except User.DoesNotExist:
        return Response({'error': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        items = MenuItem.objects.all().select_related('category', 'restaurant')
        return Response(MenuItemSerializer(items, many=True).data)
    
    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'PATCH':
        item_id = request.data.get('id')
        try:
            item = MenuItem.objects.get(pk=item_id)
            serializer = MenuItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

    elif request.method == 'DELETE':
        item_id = request.data.get('id')
        try:
            item = MenuItem.objects.get(pk=item_id)
            item.delete()
            return Response(status=204)
        except MenuItem.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)
