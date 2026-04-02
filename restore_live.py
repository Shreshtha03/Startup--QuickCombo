import paramiko
import os

def run_restore():
    print("🚀 STARTING EMERGENCY RESTORE (V4 - WITH PIP)...")
    
    host = 'ssh-quickcombo.alwaysdata.net'
    user = 'quickcombo'
    pw = 'Dinesh@061004' 
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {host}...")
        ssh.connect(host, username=user, password=pw, timeout=25)
        print("✅ Connected to AlwaysData.")
        
        sftp = ssh.open_sftp()
        base_local = r"c:\Placement project\Quickcombo"
        base_remote = "www/quickcombo_backend"

        # List of critical files to upload
        files_to_upload = [
            ("quickcombo/settings.py", "quickcombo/settings.py"),
            ("api/urls.py", "api/urls.py"),
            ("api/views.py", "api/views.py"),
            ("seed_restaurants.py", "seed_restaurants.py"),
            ("requirements.txt", "requirements.txt"),
        ]

        for local_rel, remote_rel in files_to_upload:
            local_path = os.path.join(base_local, local_rel)
            remote_path = os.path.join(base_remote, remote_rel)
            print(f"📤 Uploading {local_rel}...")
            sftp.put(local_path, remote_path)
        
        sftp.close()
        print("✅ Files uploaded.")

        # Execute Remote Commands
        commands = [
            "cd ~/www/quickcombo_backend/",
            "source venv/bin/activate",
            "pip install -r requirements.txt", # ENSURE REQUESTS IS INSTALLED
            "python manage.py migrate --noinput",
            "python seed_restaurants.py",
            "python manage.py collectstatic --noinput",
            "touch quickcombo/wsgi.py",
            "python manage.py shell -c 'from django.core.cache import cache; cache.clear(); print(\"Cache Cleared\")'"
        ]
        
        full_command = " && ".join(commands)
        print("Executing remote commands (this may take a minute)...")
        stdin, stdout, stderr = ssh.exec_command(full_command)
        
        for line in stdout:
            print(f"  [Remote] {line.strip()}")
            
        err = stderr.read().decode()
        if err:
            print(f"⚠️  Remote Output/Warning:\n{err}")
            
        print("\n✨ RESTORE FINISHED. Restarting site...")
        ssh.exec_command("touch ~/www/quickcombo_backend/quickcombo/wsgi.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        ssh.close()
        print("🔌 Connection closed.")

if __name__ == "__main__":
    run_restore()
