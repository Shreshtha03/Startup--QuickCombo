"""
DEEP DIAGNOSIS: 
- User IS staff in DB ✅
- Cache purged ✅  
- Server restarted ✅
- Still 403 ❌

The only explanation: The admin_views.py on the server has DIFFERENT code
that has altered logic - maybe checking something else, or the server is 
loading from a DIFFERENT copy of admin_views.py.

Let's check EXACTLY which admin_views.py is loaded at runtime.
"""
import paramiko
import time
import requests

HOST = "ssh-quickcombo.alwaysdata.net"
USER_SSH = "quickcombo"
PASS = "Dinesh@061004"

# We'll add a diagnostic print to admin_stats to see what's happening inside
DIAGNOSTIC_ADMIN_VIEWS = '''from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum

from api.models import User, Order, MenuItem

@api_view(['GET'])
def admin_stats(request):
    """Admin stats - DIAGNOSTIC VERSION"""
    import sys
    email = request.headers.get('X-User-Email', '')
    
    # Log what we found
    debug_info = {
        'email_received': email,
        'file_loaded': __file__,
        'sys_path': sys.path[:3],
    }
    
    if not email:
        return Response({'error': 'No email header', 'debug': debug_info}, status=401)
    
    try:
        user = User.objects.get(email=email)
        debug_info['user_found'] = True
        debug_info['is_staff'] = user.is_staff
        debug_info['is_superuser'] = user.is_superuser
        debug_info['is_active'] = user.is_active
        
        if not user.is_staff:
            return Response({'error': 'Forbidden', 'debug': debug_info}, status=403)
        
    except User.DoesNotExist:
        debug_info['user_found'] = False
        return Response({'error': 'Unauthorized', 'debug': debug_info}, status=401)

    total_sales = Order.objects.filter(status='delivered').aggregate(Sum('total'))['total__sum'] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    active_orders = Order.objects.exclude(status__in=['delivered', 'cancelled']).count()
    
    return Response({
        'total_sales': float(total_sales),
        'total_orders': int(total_orders),
        'pending_orders': int(pending_orders),
        'active_orders': int(active_orders),
        'debug': debug_info,
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
        from api.serializers import OrderSerializer
        return Response(OrderSerializer(orders, many=True).data)
    
    elif request.method == 'PATCH':
        order_id = request.data.get('order_id')
        new_status = request.data.get('status')
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            from api.serializers import OrderSerializer
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

    from api.serializers import MenuItemSerializer
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
'''

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER_SSH, password=PASS)
    print("[CONNECTED]")

    # Push diagnostic admin_views to BOTH dirs
    for root in ["/home/quickcombo/quickcombo_app", "/home/quickcombo/www/quickcombo_backend"]:
        sftp = ssh.open_sftp()
        try:
            path = f"{root}/api/admin_views.py"
            with sftp.file(path, 'w') as f:
                f.write(DIAGNOSTIC_ADMIN_VIEWS)
            print(f"  ✅ Wrote diagnostic admin_views to {root}")
        except Exception as e:
            print(f"  ❌ {root}: {e}")
        sftp.close()

    # Purge ALL cache globally
    ssh.exec_command("find /home/quickcombo -name '*.pyc' -delete 2>/dev/null || true")
    ssh.exec_command("find /home/quickcombo -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true")
    
    # Hard restart
    ssh.exec_command("killall -9 uwsgi 2>/dev/null || true")
    time.sleep(2)
    ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
    print("\n  Server restarted. Waiting 15s...")
    ssh.close()
    
    time.sleep(15)

    # Test
    print("\n[TEST] Hitting diagnostics endpoint...")
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'},
        timeout=25
    )
    print(f"  Status: {r.status_code}")
    import json
    try:
        data = r.json()
        print(f"  Response: {json.dumps(data, indent=2)}")
    except:
        print(f"  Body: {r.text[:500]}")

if __name__ == "__main__":
    main()
