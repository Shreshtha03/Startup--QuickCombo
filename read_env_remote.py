import paramiko
import os

def read_env():
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
        try:
            with sftp.file(f"{LIVE_ROOT}/.env", "r") as f:
                print("\n--- .env Content ---")
                print(f.read().decode())
        except Exception as e:
            print(f"No .env file found: {e}")
            
        print("\n--- Listing root directory ---")
        stdin, stdout, stderr = ssh.exec_command(f"ls -la {LIVE_ROOT}")
        print(stdout.read().decode())
            
        sftp.close()
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    read_env()
