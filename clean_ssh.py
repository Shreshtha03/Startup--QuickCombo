import paramiko

def run():
    print("Connecting to AlwaysData via SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=10)
        
        cmd = """
cd ~/www/quickcombo_backend/
source venv/bin/activate
python manage.py shell -c "
from api.models import Restaurant
keep_keywords = ['disco', 'chettinadu']
deleted = 0
kept = 0
for r in Restaurant.objects.all():
    if any(k in r.name.lower() for k in keep_keywords):
        kept += 1
    else:
        r.delete()
        deleted += 1
print(f'Done! Kept {kept}, Deleted {deleted}')
"
"""
        print("Executing script on the live server...")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        out = stdout.read().decode()
        err = stderr.read().decode()
        
        if out: print("Remote Output:", out)
        if err: print("Remote Error:", err)
            
    except Exception as e:
        print("SSH Error:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    run()
