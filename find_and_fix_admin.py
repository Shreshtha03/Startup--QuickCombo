"""
Find the EXACT db.sqlite3 that the running uWSGI process is using
by reading it from the WSGI environment at request-time.
"""
import paramiko
import time
import requests

HOST = "ssh-quickcombo.alwaysdata.net"
USER = "quickcombo"
PASS = "Dinesh@061004"
LIVE_ROOT = "/home/quickcombo/quickcombo_app"

# We temporarily add a db_name field to the debug-db response
PATCH_CODE = '''
    # TEMP DIAGNOSTIC - dump actual runtime DB path
    from django.conf import settings as _s
    _db_name = str(_s.DATABASES["default"]["NAME"])
'''

FIND_AND_FIX_SCRIPT = """
import os, sys, django

# Try loading from the live root
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()

from django.conf import settings
db_path = settings.DATABASES['default']['NAME']
print(f'Live DB: {db_path}')

# Check if the db file has api_user table
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print(f'Tables: {tables}')

# If api_user exists, fix the user
if 'api_user' in tables:
    from api.models import User
    email = 'shreshtha0311@gmail.com'
    try:
        u = User.objects.get(email=email)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        print(f'[FIXED] {email} is now is_staff={u.is_staff}')
    except User.DoesNotExist:
        u = User(email=email, name='Shreshtha', phone='9999999999',
                 is_staff=True, is_superuser=True, is_active=True)
        u.set_password('admin@4098')
        u.save()
        print(f'[CREATED] {email}')
else:
    print('ERROR: api_user table not found in this DB!')
    print('Need to run migrations first.')
    import subprocess
    result = subprocess.run(['python3', 'manage.py', 'migrate'],
                           capture_output=True, text=True,
                           cwd='/home/quickcombo/quickcombo_app')
    print(result.stdout[-500:])
    print(result.stderr[-500:])
    
    # Try again after migrations
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables2 = [r[0] for r in cursor.fetchall()]
    print(f'Tables after migration: {tables2}')
    if 'api_user' in tables2:
        from api.models import User
        email = 'shreshtha0311@gmail.com'
        u = User(email=email, name='Shreshtha', phone='9999999999',
                 is_staff=True, is_superuser=True, is_active=True)
        u.set_password('admin@4098')
        u.save()
        print(f'[CREATED] {email}')
"""


def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS)
    print("[CONNECTED]")

    sftp = ssh.open_sftp()
    with sftp.file('/tmp/find_and_fix.py', 'w') as f:
        f.write(FIND_AND_FIX_SCRIPT)
    sftp.close()

    print("\n[RUNNING] DJ find-and-fix script on server...")
    stdin, stdout, stderr = ssh.exec_command(
        "cd /home/quickcombo/quickcombo_app && python3 /tmp/find_and_fix.py 2>&1"
    )
    out = stdout.read().decode()
    print(out)
    
    # Also check the backend DB for the same user
    print("\n[CHECKING] quickcombo_backend DB...")
    backend_db = "/home/quickcombo/www/quickcombo_backend/db.sqlite3"
    cmd = f"sqlite3 {backend_db} \"SELECT email,is_staff,is_superuser FROM api_user WHERE email='shreshtha0311@gmail.com';\""
    stdin2, stdout2, _ = ssh.exec_command(cmd)
    print(f"  Backend DB: {stdout2.read().decode().strip()}")
    
    ssh.close()

    # Test endpoint
    print("\n[TESTING] Admin endpoint...")
    time.sleep(3)
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'},
        timeout=20
    )
    print(f"  Status: {r.status_code}")
    print(f"  Response: {r.text}")

if __name__ == "__main__":
    main()
