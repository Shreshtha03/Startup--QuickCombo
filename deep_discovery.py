import paramiko
import os

def deep_discovery():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    ROOTS = [
        "/home/quickcombo/www/quickcombo_backend",
        "/home/quickcombo/quickcombo_app"
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Deep Environment Discovery:")
        
        for root in ROOTS:
            print(f"\n--- Checking {root} ---")
            # We'll ask Django for its absolute CWD and API path
            # We'll use double-quotes carefully
            cmd = f"source {root}/venv/bin/activate && cd {root} && python3 manage.py shell -c 'import os, api; print(f\"CWD:{{os.getcwd()}}\"); print(f\"API:{{api.__file__}}\")'"
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            
            if "CWD:" in out:
                print(out)
            else:
                print(f"FAILED to query {root}. Error: {err}")
        
        print("\n--- Listing ALL environment variables ---")
        stdin, stdout, stderr = ssh.exec_command("printenv")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    deep_discovery()
