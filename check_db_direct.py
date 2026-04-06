import paramiko
import os

def check_db_direct():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        # We will create a small python script on the remote server
        # that manually loads Django settings and prints the active DB context
        remote_script = """
import os
import sys
import django

# We will test both roots to see what settings they load
def test_root(root_dir):
    try:
        print(f"\\n--- Testing ROOT: {root_dir} ---")
        sys.path.insert(0, root_dir)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
        django.setup()
        
        from django.conf import settings
        db_engine = settings.DATABASES['default']['ENGINE']
        db_name = settings.DATABASES['default']['NAME']
        print(f"ENGINE: {db_engine}")
        print(f"NAME: {db_name}")
        
        # Now try to get the user
        from api.models import User
        u = User.objects.get(email='shreshtha0311@gmail.com')
        print(f"User is_staff: {u.is_staff}, is_superuser: {u.is_superuser}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sys.path.remove(root_dir)

test_root('/home/quickcombo/quickcombo_app')
test_root('/home/quickcombo/www/quickcombo_backend')
"""
        sftp = ssh.open_sftp()
        with sftp.file('/home/quickcombo/test_django_env.py', 'w') as f:
            f.write(remote_script)
        sftp.close()
        
        print("\nExecuting remote test script...")
        stdin, stdout, stderr = ssh.exec_command("python3 /home/quickcombo/test_django_env.py")
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err:
            print("Errors:", err)
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_db_direct()
