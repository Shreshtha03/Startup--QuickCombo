import paramiko
import os

def check_real_live():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        sftp = ssh.open_sftp()
        
        print(f"\n--- backend urls.py ---")
        try:
            with sftp.file(f"/home/quickcombo/www/quickcombo_backend/api/urls.py", "r") as f:
                print(f.read().decode())
        except Exception as e:
            print(f"Error: {e}")
            
        print(f"\n--- app urls.py ---")
        try:
            with sftp.file(f"/home/quickcombo/quickcombo_app/api/urls.py", "r") as f:
                print(f.read().decode())
        except Exception as e:
            print(f"Error: {e}")
            
        # Also let's find ALL api/urls.py
        print(f"\n--- GLOBAL URLS_PY SEARCH ---")
        stdin, stdout, stderr = ssh.exec_command("find /home/quickcombo -name 'urls.py' | grep api")
        print(stdout.read().decode().strip())
        
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_real_live()
