import paramiko
import os

def inject_fatal_errors():
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
        print("Connected! Injecting Fatal Crashes...")
        
        for root, marker in ROOTS:
            settings_path = f"{root}/quickcombo/settings.py"
            # We'll use sed to insert it at the very first line
            cmd = f"sed -i \"1i crash = 1 / 0  # CRASH_MARKER: {marker}\" {settings_path}"
            ssh.exec_command(cmd)
            print(f"Injected crash into {settings_path}")
            
        print("\n--- Nuclear Restart ---")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
        ssh.exec_command("touch /home/quickcombo/quickcombo_app/quickcombo/wsgi.py")
        
        print("\n🚀 CRASH INJECTED. SITE SHOULD BE DOWN NOW.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_fatal_errors()
