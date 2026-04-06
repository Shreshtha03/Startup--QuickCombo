import paramiko
import time
import requests

HOST = "ssh-quickcombo.alwaysdata.net"
USER_SSH = "quickcombo"
PASS = "Dinesh@061004"

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER_SSH, password=PASS)
    print("[CONNECTED]")

    # Find the REAL uwsgi.py config or process
    print("\n[PROCS] Running processes:")
    stdin, stdout, _ = ssh.exec_command("ps aux | grep -E 'uwsgi|python' | grep -v grep | head -20")
    print(stdout.read().decode())
    
    # Check /home/quickcombo/www/ structure
    print("\n[WWW] Contents of /home/quickcombo/www/:")
    stdin2, stdout2, _ = ssh.exec_command("ls -la /home/quickcombo/www/")
    print(stdout2.read().decode())
    
    # Check /home/quickcombo/www/quickcombo_backend/
    print("\n[BACKEND] backend api/admin_views.py first 5 lines:")
    stdin3, stdout3, _ = ssh.exec_command("head -5 /home/quickcombo/www/quickcombo_backend/api/admin_views.py")
    print(stdout3.read().decode())
    
    # Check /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py
    print("\n[WSGI] backend wsgi.py:")
    stdin4, stdout4, _ = ssh.exec_command("cat /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
    wsgi_content = stdout4.read().decode()
    print(wsgi_content)

    # The key: what does the wsgi.py do with sys.path?
    # If it injects fresh_app, we need to fix THERE
    if "fresh_app" in wsgi_content:
        print("\n⚠️  WSGI injects /fresh_app/ — that's the live root!")
        live_root = "/home/quickcombo/fresh_app"
    elif "quickcombo_app" in wsgi_content:
        print("\n⚠️  WSGI injects /quickcombo_app/ — that's the live root!")
        live_root = "/home/quickcombo/quickcombo_app"
    else:
        print("\nℹ️  WSGI uses its own directory")
        live_root = "/home/quickcombo/www/quickcombo_backend"

    print(f"\n[LIVE ROOT] = {live_root}")
    
    # Check the user in what DB that root's settings would use
    check = f"""
import os, sys, django
sys.path.insert(0, '{live_root}')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from django.conf import settings
print('DB:', settings.DATABASES['default']['NAME'])
from api.models import User
try:
    u = User.objects.get(email='shreshtha0311@gmail.com')
    print(f'User: {{u.email}}, is_staff={{u.is_staff}}, is_superuser={{u.is_superuser}}')
except Exception as e:
    print(f'Error: {{e}}')
"""
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/final_check.py', 'w') as f:
        f.write(check)
    sftp.close()
    
    stdin5, stdout5, _ = ssh.exec_command(f"cd {live_root} && python3 /tmp/final_check.py 2>&1")
    print(f"\n[DB in LIVE ROOT]")
    print(stdout5.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    main()
