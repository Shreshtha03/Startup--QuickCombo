import paramiko
import os
import requests
import time

def full_audit_and_fix():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print("Connecting...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=user, password=password)
    print("Connected!\n")
    
    # ─── STEP 1: Find the actual DB the web process uses ───────────────────
    print("=" * 60)
    print("STEP 1: Finding actual live DB")
    print("=" * 60)
    
    test_script = """
import os, sys, django
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from django.conf import settings
db_name = settings.DATABASES['default']['NAME']
print(f"DB: {db_name}")
from django.db import connection
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cursor.fetchall()]
print(f"TABLES: {tables}")
"""
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/test_db.py', 'w') as f:
        f.write(test_script)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command("python3 /tmp/test_db.py 2>&1")
    result = stdout.read().decode()
    print(result)
    
    # ─── STEP 2: Run migrations & create user in quickcombo_app DB ─────────
    print("=" * 60)
    print("STEP 2: Running migrations in quickcombo_app")
    print("=" * 60)
    
    stdin, stdout, stderr = ssh.exec_command(
        "cd /home/quickcombo/quickcombo_app && python3 manage.py migrate 2>&1"
    )
    mig_result = stdout.read().decode()
    print(mig_result[-1000:])  # last 1000 chars
    
    # ─── STEP 3: Grant shreshtha staff in both DBs ──────────────────────────
    print("=" * 60)
    print("STEP 3: Granting admin privileges in quickcombo_app DB")
    print("=" * 60)
    
    grant_script = """
import os, sys, django
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from api.models import User
email = 'shreshtha0311@gmail.com'
try:
    u = User.objects.get(email=email)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"SUCCESS: {email} is now staff={u.is_staff}, superuser={u.is_superuser}")
except User.DoesNotExist:
    print(f"User {email} not found - creating...")
    u = User.objects.create(
        email=email, 
        name='Shreshtha',
        phone='9999999999',
        is_staff=True,
        is_superuser=True
    )
    u.set_password('admin@4098')
    u.save()
    print(f"CREATED: {email}")
"""
    
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/grant_admin.py', 'w') as f:
        f.write(grant_script)
    sftp.close()
    
    stdin, stdout, stderr = ssh.exec_command("python3 /tmp/grant_admin.py 2>&1")
    print(stdout.read().decode())
    
    # ─── STEP 4: Also update the www/quickcombo_backend DB ─────────────────
    print("=" * 60)
    print("STEP 4: Doing the same in quickcombo_backend DB")
    print("=" * 60)
    
    cmd = "sqlite3 /home/quickcombo/www/quickcombo_backend/db.sqlite3 \"UPDATE api_user SET is_staff=1, is_superuser=1 WHERE email='shreshtha0311@gmail.com';\""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    time.sleep(2)
    
    # Verify
    cmd2 = "sqlite3 /home/quickcombo/www/quickcombo_backend/db.sqlite3 \"SELECT email, is_staff, is_superuser FROM api_user WHERE email='shreshtha0311@gmail.com';\""
    stdin2, stdout2, stderr2 = ssh.exec_command(cmd2)
    print(f"quickcombo_backend DB user: {stdout2.read().decode()}")
    
    ssh.close()
    
    # ─── STEP 5: Test the endpoint ──────────────────────────────────────────
    print("=" * 60)
    print("STEP 5: Final endpoint test")
    print("=" * 60)
    
    time.sleep(5)
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'}
    )
    print(f"Admin stats endpoint: {r.status_code}")
    print(r.text)

if __name__ == "__main__":
    full_audit_and_fix()
