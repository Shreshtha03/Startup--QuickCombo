import paramiko
import os

def grant_staff():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    LIVE_ROOT = "/home/quickcombo/quickcombo_app"
    email = "shreshtha0311@gmail.com"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        # Granting staff directly via a reliable shell command
        cmd = f"cd {LIVE_ROOT} && python3 manage.py shell -c \"from api.models import User; u=User.objects.get(email='{email}'); u.is_staff=True; u.is_superuser=True; u.save(); print('✅ {email} IS NOW STAFF')\""
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()
        
        if result:
            print(result)
        if errors:
            print(f"⚠️ Errors: {errors}")
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    grant_staff()
