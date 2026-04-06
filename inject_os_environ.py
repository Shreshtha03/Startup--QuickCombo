import paramiko
import os
import requests
import time

def inject_os_environ():
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
        view_path = f"{LIVE_ROOT}/api/views.py"
        
        with sftp.file(view_path, "r") as f:
            content = f.read().decode()
            
        print("Injecting environment variables into debug_db...")
        new_content = content.replace(
            '"error": None,', 
            '"error": None, "my_env_db": os.environ.get("DATABASE_URL", "NOT_SET"), "db_engine": settings.DATABASES["default"]["ENGINE"], "db_name": str(settings.DATABASES["default"]["NAME"]),'
        )
        
        with sftp.file(view_path, "w") as f:
            f.write(new_content)
        print("✅ Injected.")
        sftp.close()
        
        print("Restarting uWSGI...")
        ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.close()
        
        print("Waiting 10 seconds...")
        time.sleep(10)
        
        r = requests.get('https://quickcombo.alwaysdata.net/api/debug-db/')
        print(f"Live Debug DB:\n{r.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_os_environ()
