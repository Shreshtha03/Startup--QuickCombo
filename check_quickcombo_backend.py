import paramiko
import os

def check_backend_dir():
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
        print(f"\n--- Reading {LIVE_ROOT}/api/admin_views.py ---")
        try:
            with sftp.file(f"{LIVE_ROOT}/api/admin_views.py", "r") as f:
                print(f.read().decode())
        except Exception as e:
            print(f"Missing admin_views! Error: {e}")
            
        print(f"\n--- Checking if shreshtha0311 is staff ---")
        cmd = f"sqlite3 {LIVE_ROOT}/db.sqlite3 \"SELECT email, is_staff, is_superuser FROM api_user WHERE email='shreshtha0311@gmail.com';\""
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("SQL RESPONSE:", stdout.read().decode())
            
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_backend_dir()
