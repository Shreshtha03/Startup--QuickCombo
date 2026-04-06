import paramiko
import os

def find_all_settings():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Global Search for settings.py:")
        
        # This will find EVERYTHING
        cmd = "find /home/quickcombo/ -name 'settings.py'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        results = stdout.read().decode().strip()
        
        if results:
            print("\n--- SETTINGS FILES FOUND ---")
            print(results)
        else:
            print("\n--- NO SETTINGS FILES FOUND (IMPOSSIBLE!) ---")
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_all_settings()
