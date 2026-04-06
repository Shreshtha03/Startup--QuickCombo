import paramiko
import os

def final_sync_urls():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    # THE DEFINITIVELY PROVEN LIVE DIRECTORY
    LIVE_ROOT = "/home/quickcombo/quickcombo_app"
    
    URLS_PY = '''from django.urls import path
from . import views

urlpatterns = [
    # ADMIN DASHBOARD (MATCHING FRONTEND)
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

    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print(f"Connected! Applying FINAL URLs to {LIVE_ROOT}/api/urls.py...")
        
        sftp = ssh.open_sftp()
        with sftp.file(f"{LIVE_ROOT}/api/urls.py", "w") as f:
            f.write(URLS_PY)
        print("✅ URLS_PY UPDATED")
        sftp.close()
        
        print("\n--- Hard Restart ---")
        ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("killall -9 python3 || true")
        
        print("\n🚀 FINAL SYNC COMPLETE.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    final_sync_urls()
