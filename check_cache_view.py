import paramiko
import os

def check_cache():
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
        print(f"\n--- Reading {LIVE_ROOT}/api/views.py ---")
        try:
            with sftp.file(f"{LIVE_ROOT}/api/views.py", "r") as f:
                content = f.read().decode()
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "def debug_db" in line:
                        start = max(0, i-5)
                        end = min(len(lines), i+20)
                        for j in range(start, end):
                            print(f"{j+1}: {lines[j]}")
        except Exception as e:
            print(f"Error: {e}")
            
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_cache()
