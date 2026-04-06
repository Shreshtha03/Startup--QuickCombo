import paramiko
import os

def inject_identity_probes():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    DIR_MARKERS = [
        ("/home/quickcombo/www/quickcombo_backend", "WWW"),
        ("/home/quickcombo/quickcombo_app", "APP")
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Injecting probes...")
        
        for root, marker in DIR_MARKERS:
            settings_path = f"{root}/quickcombo/settings.py"
            # Add a setting that we can verify via shell or headers
            # We'll use a unique CACHE prefix to identify the root
            cmd = f"echo \"ID_MARKER = '{marker}'\" >> {settings_path}"
            ssh.exec_command(cmd)
            print(f"Injected {marker} into {settings_path}")
            
        print("\n--- Restarting Site ---")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
        ssh.exec_command("touch /home/quickcombo/quickcombo_app/quickcombo/wsgi.py")
        
        print("\n🚀 PROBES INJECTED. PROCEEDING TO VERIFICATION.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_identity_probes()
