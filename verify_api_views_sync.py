import paramiko
import os

def check_views_and_urls():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    LIVE_ROOT = "/home/quickcombo/quickcombo_app"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        sftp = ssh.open_sftp()
        
        # 1. Read api/urls.py
        print(f"\n--- {LIVE_ROOT}/api/urls.py ---")
        with sftp.file(f"{LIVE_ROOT}/api/urls.py", "r") as f:
            print(f.read().decode())
            
        # 2. Read api/views.py
        print(f"\n--- {LIVE_ROOT}/api/views.py ---")
        with sftp.file(f"{LIVE_ROOT}/api/views.py", "r") as f:
            content = f.read().decode()
            print(content[:500] + "...")
            if "from .admin_views import" in content or "from api.admin_views import" in content:
                print("\n✅ Admin views are imported in views.py")
            else:
                print("\n❌ CRITICAL: admin_views are NOT imported in views.py!")

        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_views_and_urls()
