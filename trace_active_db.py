import paramiko
import os
import requests
import time

def trace_db():
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
        # Modifying views.py to return the DB path in the debug-db endpoint
        view_path = f"{LIVE_ROOT}/api/views.py"
        with sftp.file(view_path, "r") as f:
            content = f.read().decode()
            
        if '"db_path":' not in content:
            print("Injecting Trace DB Path...")
            # Injecting at the end of the debug_db dict
            new_content = content.replace('"error": None,', '"error": None, "db_path": str(settings.DATABASES["default"]["NAME"]),')
            with sftp.file(view_path, "w") as f:
                f.write(new_content)
            print("✅ Injected.")
            
            print("Restarting uWSGI...")
            ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
            ssh.exec_command("killall -9 uwsgi || true")
            time.sleep(5)
            
        sftp.close()
        
        print("\n--- Querying Live DB Path ---")
        r = requests.get('https://quickcombo.alwaysdata.net/api/debug-db/')
        data = r.json()
        active_db = data.get("db_path")
        print(f"ACTIVE DB IS: {active_db}")
        
        if active_db:
            # APPLY THE FINAL SQL TO THE ACTUAL FILE
            print(f"\nUPDATING AUTH IN {active_db}...")
            email = "shreshtha0311@gmail.com"
            sql = f"UPDATE api_user SET is_staff=1, is_superuser=1 WHERE email='{email}';"
            cmd = f"sqlite3 {active_db} \"{sql}\""
            ssh.exec_command(cmd)
            print("✅ Permissions granted.")
            
        ssh.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    trace_db()
