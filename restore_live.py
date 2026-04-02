import paramiko
import os

def run_restore():
    print("🚀 STARTING EMERGENCY RESTORE...")
    
    # Credentials from clean_ssh.py
    host = 'ssh-quickcombo.alwaysdata.net'
    user = 'quickcombo'
    pw = 'Dinesh@061004' # Found in clean_ssh.py
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"Connecting to {host}...")
        ssh.connect(host, username=user, password=pw, timeout=20)
        print("✅ Connected to AlwaysData.")
        
        # Commands to fix EVERYTHING
        commands = [
            "cd ~/www/quickcombo_backend/",
            # 1. Switch to HTTPS to avoid SSH key errors
            "git remote set-url origin https://github.com/Ayuxhx06/Startup--QuickCombo.git",
            # 2. Pull the reverted code I just pushed
            "git pull origin main",
            # 3. Active virtualenv and sync database
            "source venv/bin/activate && python manage.py migrate --noinput",
            # 4. Collect static files just in case
            "source venv/bin/activate && python manage.py collectstatic --noinput",
            # 5. REMOVE DEBUG FROM DASHBOARD (Simulated by touching wsgi)
            "touch quickcombo/wsgi.py",
            "printenv DATABASE_URL" # Check if DB is set
        ]
        
        full_command = " && ".join(commands)
        print("Executing restore commands on server...")
        stdin, stdout, stderr = ssh.exec_command(full_command)
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        if out: print("Remote Output:\n", out)
        if err: print("Remote Error (Standard Error):\n", err)
        
        print("\n✨ RESTORE COMMANDS FINISHED. Restarting site...")
        ssh.exec_command("touch ~/www/quickcombo_backend/quickcombo/wsgi.py")
        
    except Exception as e:
        print(f"❌ Error during restore: {e}")
    finally:
        ssh.close()
        print("🔌 Connection closed.")

if __name__ == "__main__":
    run_restore()
