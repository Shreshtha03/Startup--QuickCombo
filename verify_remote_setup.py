import paramiko
import os
import requests

def verify_remote_setup():
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
        
        # 1. Check api/urls.py
        print(f"\n--- {LIVE_ROOT}/api/urls.py ---")
        sftp = ssh.open_sftp()
        with sftp.file(f"{LIVE_ROOT}/api/urls.py", "r") as f:
            print(f.read().decode())
        
        # 2. Check api/admin_views.py
        print(f"\n--- {LIVE_ROOT}/api/admin_views.py ---")
        try:
            with sftp.file(f"{LIVE_ROOT}/api/admin_views.py", "r") as f:
                print(f.read().decode()[:200] + "...")
        except:
            print("❌ api/admin_views.py MISSING in check!")
            
        sftp.close()
        ssh.close()
        
        # 3. Live Endpoint Verification
        print("\n--- Live Endpoint Checks ---")
        endpoints = [
            "/api/admin/stats/",
            "/api/admin-dashboard/stats/",
            "/api/debug-db/"
        ]
        for ep in endpoints:
            url = f"https://quickcombo.alwaysdata.net{ep}"
            r = requests.get(url)
            print(f"{url} -> {r.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_remote_setup()
