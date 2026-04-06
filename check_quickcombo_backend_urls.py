import paramiko
import os

def check_backend_urls():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    LIVE_ROOT = "/home/quickcombo/www/quickcombo_backend"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        sftp = ssh.open_sftp()
        print(f"\n--- Reading {LIVE_ROOT}/api/urls.py ---")
        try:
            with sftp.file(f"{LIVE_ROOT}/api/urls.py", "r") as f:
                print(f.read().decode())
        except Exception as e:
            print(f"Missing urls.py! Error: {e}")
            
        print(f"\n--- Reading {LIVE_ROOT}/quickcombo/wsgi.py ---")
        try:
            with sftp.file(f"{LIVE_ROOT}/quickcombo/wsgi.py", "r") as f:
                print(f.read().decode())
        except Exception as e:
            print(f"Missing wsgi.py! Error: {e}")
            
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_backend_urls()
