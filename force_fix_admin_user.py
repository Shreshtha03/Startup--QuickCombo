"""
The problem: 
- quickcombo_app/db.sqlite3 is used by the live server (confirmed)
- Migrations ran, user 'shreshtha0311@gmail.com' was CREATED (in that DB)  
- But endpoint still returns 403 "Forbidden"

Root cause: The user was created without 'is_staff=True' (the script created it but
the category 'is_api_user' table didn't have categories filled in).
Let's verify and forcibly fix the user in the exact db file.
"""
import paramiko
import time
import requests

HOST = "ssh-quickcombo.alwaysdata.net"
USER_SSH = "quickcombo"
PASS = "Dinesh@061004"

FIX_SCRIPT = """
import os, sys, django
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()

from api.models import User
email = 'shreshtha0311@gmail.com'

# Check current state
try:
    u = User.objects.get(email=email)
    print(f"BEFORE: email={u.email}, is_staff={u.is_staff}, is_superuser={u.is_superuser}, is_active={u.is_active}")
    
    # Force update
    User.objects.filter(email=email).update(
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    
    # Verify
    u.refresh_from_db()
    print(f"AFTER:  email={u.email}, is_staff={u.is_staff}, is_superuser={u.is_superuser}, is_active={u.is_active}")
    
except User.DoesNotExist:
    print(f"User {email} NOT FOUND!")
    # List all users
    all_users = User.objects.all()
    print(f"All users: {list(all_users.values('email', 'is_staff', 'is_superuser'))}")
"""

def main():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER_SSH, password=PASS)
    print("[CONNECTED]")

    sftp = ssh.open_sftp()
    with sftp.file('/tmp/force_fix_user.py', 'w') as f:
        f.write(FIX_SCRIPT)
    sftp.close()

    print("\n[RUNNING] Force-fixing user...")
    stdin, stdout, stderr = ssh.exec_command(
        "cd /home/quickcombo/quickcombo_app && python3 /tmp/force_fix_user.py 2>&1"
    )
    out = stdout.read().decode().strip()
    print(out)

    ssh.close()

    # Also direct SQL
    ssh2 = paramiko.SSHClient()
    ssh2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh2.connect(HOST, username=USER_SSH, password=PASS)
    
    db_file = "/home/quickcombo/quickcombo_app/db.sqlite3"
    stdin2, stdout2, _ = ssh2.exec_command(
        f"sqlite3 {db_file} \"SELECT id,email,is_staff,is_superuser,is_active FROM api_user;\""
    )
    print(f"\n[DB CONTENTS]\n{stdout2.read().decode().strip()}")
    ssh2.close()

    print("\n[TESTING] Admin endpoint...")
    time.sleep(3)
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'},
        timeout=20
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")

if __name__ == "__main__":
    main()
