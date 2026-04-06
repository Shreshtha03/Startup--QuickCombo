import paramiko
import os

def hardcoded_repair_final():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    # THE CONFIRMED LIVE DIRECTORY VIA SHELL METADATA
    LIVE_ROOT = "/home/quickcombo/www/quickcombo_backend"
    
    # ─── BUFFERS (COLLISION-FREE NAMESPACE) ──────────────────────────────────────────────────
    
    URLS_PY = '''from django.urls import path
from . import views

urlpatterns = [
    # ADMIN DASHBOARD (COLLISION-FREE)
    path("admin-dashboard/stats/", views.admin_stats),
    path("admin-dashboard/orders/", views.admin_orders),
    path("admin-dashboard/menu/", views.admin_menu_items),

    # Auth
    path("auth/send-otp/", views.send_otp),
    path("auth/verify-otp/", views.verify_otp),

    # User
    path("user/profile/", views.user_profile),
    path("user/addresses/", views.user_addresses),

    # Menu
    path("menu/", views.menu_list),
    path("menu/<int:pk>/", views.menu_item_detail),
    path("categories/", views.categories_list),
    path("restaurants/", views.restaurant_list),

    # Orders
    path("orders/", views.order_list),
    path("orders/active/", views.active_order),
    path("orders/place/", views.place_order),
    path("orders/<int:order_id>/", views.order_detail),
    path("orders/<int:order_id>/tracking/", views.order_tracking),
    path("debug-db/", views.debug_db),

    # Location
    path("location/autocomplete/", views.location_autocomplete),
    path("location/reverse/", views.reverse_geocode),

    # Weather
    path("weather/", views.weather),
]
'''

    ADMIN_VIEWS_PY = '''from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from api.models import User, Order, MenuItem, Restaurant, Category
from api.serializers import OrderSerializer, MenuItemSerializer, RestaurantSerializer, CategorySerializer

@api_view(["GET"])
def admin_stats(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff: return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist: return Response({"error": "Unauthorized"}, status=401)

    total_sales = Order.objects.filter(status="delivered").aggregate(Sum("total"))["total__sum"] or 0
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    active_orders = Order.objects.exclude(status__in=["delivered", "cancelled"]).count()
    
    return Response({
        "total_sales": float(total_sales),
        "total_orders": int(total_orders),
        "pending_orders": int(pending_orders),
        "active_orders": int(active_orders),
    })

@api_view(["GET", "PATCH"])
def admin_orders(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff: return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist: return Response({"error": "Unauthorized"}, status=401)

    if request.method == "GET":
        orders = Order.objects.all().order_by("-created_at")
        return Response(OrderSerializer(orders, many=True).data)
    elif request.method == "PATCH":
        order_id = request.data.get("order_id")
        new_status = request.data.get("status")
        try:
            order = Order.objects.get(pk=order_id)
            order.status = new_status
            order.save()
            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist: return Response({"error": "Not found"}, status=404)

@api_view(["GET", "POST", "PATCH", "DELETE"])
def admin_menu_items(request):
    email = request.headers.get("X-User-Email", "")
    try:
        user = User.objects.get(email=email)
        if not user.is_staff: return Response({"error": "Forbidden"}, status=403)
    except User.DoesNotExist: return Response({"error": "Unauthorized"}, status=401)

    if request.method == "GET":
        items = MenuItem.objects.all().select_related("category", "restaurant")
        return Response(MenuItemSerializer(items, many=True).data)
    elif request.method == "POST":
        s = MenuItemSerializer(data=request.data); s.is_valid() and s.save(); return Response(s.data if s.is_valid() else s.errors, status=201 if s.is_valid() else 400)
    elif request.method == "PATCH":
        item_id = request.data.get("id")
        try:
            item = MenuItem.objects.get(pk=item_id)
            s = MenuItemSerializer(item, data=request.data, partial=True); s.is_valid() and s.save(); return Response(s.data if s.is_valid() else s.errors)
        except MenuItem.DoesNotExist: return Response({"error": "Not found"}, status=404)
    elif request.method == "DELETE":
        item_id = request.data.get("id")
        try: MenuItem.objects.get(pk=item_id).delete(); return Response(status=204)
        except MenuItem.DoesNotExist: return Response({"error": "Not found"}, status=404)
'''

    # ─── EXECUTION ───────────────────────────────────────────────────────────
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print(f"Connected! Overwriting {LIVE_ROOT} folder...")
        
        sftp = ssh.open_sftp()
        uploads = [
            ("api/urls.py", URLS_PY),
            ("api/admin_views.py", ADMIN_VIEWS_PY),
        ]
        
        for path, content in uploads:
            remote_path = f"{LIVE_ROOT}/{path}"
            print(f"Writing {remote_path}...")
            with sftp.file(remote_path, "w") as f:
                f.write(content)
            print("✅ OK")
            
        sftp.close()
        
        print("\\n--- Purging Cache & Site Restart ---")
        ssh.exec_command(f"find {LIVE_ROOT} -name '__pycache__' -type d -exec rm -rf {{}} +")
        ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("killall -9 python3 || true")
        
        print("\\n🚀 TARGETED REPAIR COMPLETE.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    hardcoded_repair_final()
