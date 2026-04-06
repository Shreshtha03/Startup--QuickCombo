import paramiko
import os
import requests
import time

def final_verify():
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
        
        print(f"\n--- Reading {LIVE_ROOT}/api/urls.py ---")
        sftp = ssh.open_sftp()
        with sftp.file(f"{LIVE_ROOT}/api/urls.py", "r") as f:
            content = f.read().decode()
            print(content)
        sftp.close()
        
        # We'll touch and wait
        print("\n--- Triggering Restart Again ---")
        ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.close()
        
        print("\nWaiting 10 seconds for reload...")
        time.sleep(10)
        
        print("\n--- Final Test ---")
        urls = [
            'https://quickcombo.alwaysdata.net/api/admin-dashboard/stats/',
            'https://quickcombo.alwaysdata.net/api/admin/stats/'
        ]
        for url in urls:
            r = requests.get(url)
            print(f"{url} -> {r.status_code}")
            if r.status_code != 404:
                print(f"SUCCESS! {url} is live.")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    final_verify()
