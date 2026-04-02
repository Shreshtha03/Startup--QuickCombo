import paramiko

def robust_deploy():
    print("🚀 Running ROBUST deployment on AlwaysData...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=15)
        
        commands = [
            "cd ~/www/quickcombo_backend/",
            "git fetch origin",
            "git reset --hard origin/main",  # FORCES the server to match GitHub
            "touch quickcombo/wsgi.py",      # Forces reload
            "source venv/bin/activate && python manage.py shell -c 'from django.core.cache import cache; cache.clear()'",
            "sleep 3",
            "curl -L -X GET https://quickcombo.alwaysdata.net/api/debug-db/"
        ]
        
        full_cmd = " && ".join(commands)
        stdin, stdout, stderr = ssh.exec_command(full_cmd)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("✅ OUTPUT:\n", output)
        if error:
            print("⚠️ ERROR:\n", error)
            
    except Exception as e:
        print("❌ SSH Error:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    robust_deploy()
