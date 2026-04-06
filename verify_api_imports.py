import paramiko
import os

def verify_api_imports():
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
        
        # Check api/views.py EXACT content
        print(f"\n--- Reading {LIVE_ROOT}/api/views.py (TOP) ---")
        with sftp.file(f"{LIVE_ROOT}/api/views.py", "r") as f:
            content = f.read().decode()
            print(content[:1500])
            
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_api_imports()
