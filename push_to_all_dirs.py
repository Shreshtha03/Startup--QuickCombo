import paramiko
import time
import requests

HOST = "ssh-quickcombo.alwaysdata.net"
USER_SSH = "quickcombo"
PASS = "Dinesh@061004"

# The CORRECT admin_views with our custom header auth (no DRF permissions)
CLEAN_ADMIN_VIEWS = '''from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum

from api.models import User, Order, MenuItem

@api_view(["GET"])
def admin_stats(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist:
        return Response({"error": "Unauthorized"}, status=401)

    total_sales = Order.objects.filter(status="delivered").aggregate(Sum("total"))["total__sum"] or 0
    return Response({
        "total_sales": float(total_sales),
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="pending").count(),
        "active_orders": Order.objects.exclude(status__in=["delivered", "cancelled"]).count(),
    })

@api_view(["GET", "PATCH"])
def admin_orders(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist:
        return Response({"error": "Unauthorized"}, status=401)

    if request.method == "GET":
        from api.serializers import OrderSerializer
        orders = Order.objects.all().order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)
    elif request.method == "PATCH":
        order_id = request.data.get("order_id")
        new_status = request.data.get("status")
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            from api.serializers import OrderSerializer
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

@api_view(["GET", "POST", "PATCH", "DELETE"])
def admin_menu_items(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff:
            return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist:
        return Response({"error": "Unauthorized"}, status=401)

    from api.serializers import MenuItemSerializer
    if request.method == "GET":
        items = MenuItem.objects.all().select_related("category", "restaurant")
        return Response(MenuItemSerializer(items, many=True).data)
    elif request.method == "POST":
        s = MenuItemSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=201)
        return Response(s.errors, status=400)
    elif request.method == "PATCH":
        item_id = request.data.get("id")
        try:
            item = MenuItem.objects.get(pk=item_id)
            s = MenuItemSerializer(item, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(s.data)
            return Response(s.errors, status=400)
        except MenuItem.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
    elif request.method == "DELETE":
        item_id = request.data.get("id")
        try:
            MenuItem.objects.get(pk=item_id).delete()
            return Response(status=204)
        except MenuItem.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
'''

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER_SSH, password=PASS)
    print("[CONNECTED]")

    # Push clean admin_views to ALL possible directories (belt + suspenders + tape)
    targets = [
        "/home/quickcombo/quickcombo_app/api/admin_views.py",
        "/home/quickcombo/www/quickcombo_backend/api/admin_views.py",
        "/home/quickcombo/fresh_app/quickcombo_app/api/admin_views.py",
        "/home/quickcombo/fresh_app/api/admin_views.py",
    ]
    
    sftp = ssh.open_sftp()
    for path in targets:
        try:
            with sftp.file(path, 'w') as f:
                f.write(CLEAN_ADMIN_VIEWS)
            print(f"  ✅ {path}")
        except Exception as e:
            print(f"  ⚠️  {path}: {e}")
    sftp.close()

    # Purge ALL pyc files globally
    print("\n[PURGE] Global pyc purge...")
    ssh.exec_command("find /home/quickcombo -name '*.pyc' -delete 2>/dev/null")
    ssh.exec_command("find /home/quickcombo -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true")
    time.sleep(1)
    
    # Restart
    print("[RESTART]")
    ssh.exec_command("killall -9 uwsgi 2>/dev/null || true")
    ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
    ssh.exec_command("touch /home/quickcombo/fresh_app/quickcombo_app/quickcombo/wsgi.py 2>/dev/null || true")
    ssh.close()
    
    print("Waiting 15s for reload...")
    time.sleep(15)
    
    # Test endpoints
    print("\n[FINAL TEST]")
    headers = {"X-User-Email": "shreshtha0311@gmail.com"}
    for url in [
        "https://quickcombo.alwaysdata.net/api/debug-db/",
        "https://quickcombo.alwaysdata.net/api/admin/stats/",
        "https://quickcombo.alwaysdata.net/api/admin/orders/",
    ]:
        r = requests.get(url, headers=headers, timeout=20)
        icon = "✅" if r.status_code == 200 else "❌"
        print(f"  {icon} [{r.status_code}] {url.split('/api/')[-1]}")
        if r.status_code == 200:
            import json
            try:
                data = r.json()
                keys = list(data.keys()) if isinstance(data, dict) else 'list'
                print(f"       Keys: {keys}")
            except: pass
        else:
            print(f"       {r.text[:150]}")

if __name__ == "__main__":
    main()
