import paramiko
import os

def find_debug_db():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Global GREP for debug_db definition:")
        
        # Searching for the specific debug_db view to find the REAL views.py
        cmd = "grep -r 'debug_db' /home/quickcombo/"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        results = stdout.read().decode().strip()
        
        if results:
            print("\n--- OCCURRENCES FOUND ---")
            print(results)
        else:
            print("\n--- NO OCCURRENCES FOUND ---")
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_debug_db()
