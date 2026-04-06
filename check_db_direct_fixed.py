import paramiko
import os

def check_db_direct_fixed():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        # Test 1
        remote_script_1 = """
import os
import sys
import django
root_dir = '/home/quickcombo/quickcombo_app'
sys.path.insert(0, root_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from django.conf import settings
print(f"NAME1: {settings.DATABASES['default']['NAME']}")
try:
    from api.models import User
    u = User.objects.get(email='shreshtha0311@gmail.com')
    print(f"User1 is_staff: {u.is_staff}")
except Exception as e:
    print(f"User1 Error: {e}")
"""
        # Test 2
        remote_script_2 = """
import os
import sys
import django
root_dir = '/home/quickcombo/www/quickcombo_backend'
sys.path.insert(0, root_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from django.conf import settings
print(f"NAME2: {settings.DATABASES['default']['NAME']}")
try:
    from api.models import User
    u = User.objects.get(email='shreshtha0311@gmail.com')
    print(f"User2 is_staff: {u.is_staff}")
except Exception as e:
    print(f"User2 Error: {e}")
"""
        sftp = ssh.open_sftp()
        with sftp.file('/home/quickcombo/test_django_env_1.py', 'w') as f:
            f.write(remote_script_1)
        with sftp.file('/home/quickcombo/test_django_env_2.py', 'w') as f:
            f.write(remote_script_2)
        sftp.close()
        
        print("\nExecuting Test 1...")
        stdin, stdout, stderr = ssh.exec_command("python3 /home/quickcombo/test_django_env_1.py")
        print(stdout.read().decode())
        
        print("\nExecuting Test 2...")
        stdin, stdout, stderr = ssh.exec_command("python3 /home/quickcombo/test_django_env_2.py")
        print(stdout.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_db_direct_fixed()
