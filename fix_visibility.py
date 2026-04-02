import paramiko

def clear_cache_and_verify():
    print("🚀 Connecting to AlwaysData to fix data visibility...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=15)
        
        # Commands to:
        # 1. Clear django cache
        # 2. Check current Database being used
        # 3. Check Restaurant count
        commands = [
            "cd ~/www/quickcombo_backend/",
            "source venv/bin/activate",
            "cat ~/err.txt | tail -n 20",
            "python manage.py shell -c 'from django.core.cache import cache; cache.clear(); print(\"Cache Cleared!\")'",
            "python manage.py shell -c 'from api.models import Restaurant; print(f\"Count: {Restaurant.objects.count()}\")'"
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
    clear_cache_and_verify()
