import paramiko
import os

def find_all_urls():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Global GREP for urls.py content:")
        
        # Searching for the specific auth route to find the REAL urls.py
        cmd = "grep -r 'auth/send-otp/' /home/quickcombo/"
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
    find_all_urls()
