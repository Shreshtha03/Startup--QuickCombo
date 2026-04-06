import paramiko
import requests
import time

def trace_active_path():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print("--- Triggering Traffic ---")
    try:
        r = requests.get('https://www.quickcombo.in/api/menu/')
        print(f"Site access status: {r.status_code}")
    except Exception as e:
        print(f"Traffic trigger failed: {e}")

    # Wait for logs to flush
    time.sleep(2)
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Searching for DEBUG_TRACE in logs...")
        
        # Search in ALL logs recursively
        cmd = "grep -r 'DEBUG_TRACE' ~/admin/logs/"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        results = stdout.read().decode().strip()
        
        if results:
            print("\n--- TRACE FOUND! ---")
            print(results)
        else:
            print("\n--- NO TRACE FOUND IN uWSGI/HTTP LOGS ---")
            print("Checking if Django is running as a custom process...")
            ssh.exec_command("ps aux | grep python")
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    trace_active_path()
