import paramiko
import os

def find_live_root():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    ROOTS = [
        "/home/quickcombo/quickcombo_app",
        "/home/quickcombo/www/quickcombo_backend"
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Path Discovery:")
        
        for root in ROOTS:
            print(f"\n--- Checking {root} ---")
            # Discover absolute path of 'api' module
            cmd = f"source {root}/venv/bin/activate && cd {root} && python3 manage.py shell -c 'import api; print(f\"TRUE_PATH:{{api.__file__}}\")'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            
            if "TRUE_PATH" in out:
                print(out)
            else:
                print(f"FAILED to query {root}. Error: {err}")
        
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_live_root()
