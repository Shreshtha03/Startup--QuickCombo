import paramiko
import os

def inject_timeout_probes():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    ROOTS = [
        ("/home/quickcombo/www/quickcombo_backend", "WWW"),
        ("/home/quickcombo/quickcombo_app", "APP")
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Injecting Timeout Sleeps...")
        
        for root, marker in ROOTS:
            urls_path = f"{root}/api/urls.py"
            # Insert at line 1
            cmd = f"sed -i '1i import time; time.sleep(300) # TIMEOUT_MARKER: {marker}' {urls_path}"
            ssh.exec_command(cmd)
            print(f"Injected timeout into {urls_path}")
            
        print("\n--- Nuclear Restart ---")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
        ssh.exec_command("touch /home/quickcombo/quickcombo_app/quickcombo/wsgi.py")
        
        print("\n🚀 SLEEPS INJECTED. SITE SHOULD HANG NOW.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_timeout_probes()
