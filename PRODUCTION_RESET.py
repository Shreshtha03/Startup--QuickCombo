"""
PRODUCTION RESET SCRIPT
=======================
Pushes clean local code to both production directories,
ensures admin user is correct in both DBs,
purges all cache, and restarts uWSGI.
"""
import paramiko
import os
import time
import requests

# ─── SSH Credentials ──────────────────────────────────────────────────────────
HOST = "ssh-quickcombo.alwaysdata.net"
USER = "quickcombo"
PASS = "Dinesh@061004"

# ─── Production directories ────────────────────────────────────────────────────
# The WSGI config in quickcombo_backend injects quickcombo_app into sys.path,
# so CODE from quickcombo_app runs. But we must also keep quickcombo_backend clean.
DIRS = [
    "/home/quickcombo/quickcombo_app",
    "/home/quickcombo/www/quickcombo_backend",
]
ADMIN_EMAIL = "shreshtha0311@gmail.com"

# ─── Read local files ─────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))

def read_local(rel_path):
    with open(os.path.join(BASE, rel_path), "r", encoding="utf-8") as f:
        return f.read()

FILES_TO_SYNC = {
    "api/urls.py":         read_local("api/urls.py"),
    "api/views.py":        read_local("api/views.py"),
    "api/admin_views.py":  read_local("api/admin_views.py"),
    "api/models.py":       read_local("api/models.py"),
    "api/serializers.py":  read_local("api/serializers.py"),
    "quickcombo/urls.py":  read_local("quickcombo/urls.py"),
}

# ─── The clean WSGI for quickcombo_app (no path injections needed here) ────────
WSGI_CLEAN = '''import sys, os
BASE_DIR = '/home/quickcombo/quickcombo_app'
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickcombo.settings')
application = get_wsgi_application()
'''

# Grant admin script (run on remote)
GRANT_ADMIN_SCRIPT = f"""
import os, sys, django
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()
from api.models import User
email = '{ADMIN_EMAIL}'
try:
    u = User.objects.get(email=email)
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print(f"[OK] {{email}} -> is_staff={{u.is_staff}}, is_superuser={{u.is_superuser}}")
except User.DoesNotExist:
    print(f"[NOT FOUND] {{email}} — creating superuser...")
    u = User(email=email, name='Shreshtha', phone='9999999999', is_staff=True, is_superuser=True, is_active=True)
    u.set_password('admin@4098')
    u.save()
    print(f"[CREATED] {{email}}")
"""


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def main():
    print(">>> QUICKCOMBO PRODUCTION RESET <<<")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, username=USER, password=PASS)
    print(f"[CONNECTED] {HOST}")
    sftp = ssh.open_sftp()

    # ── STEP 1: Push clean files to both directories ──────────────────────────
    section("STEP 1: Syncing clean local code to production")
    for remote_dir in DIRS:
        print(f"\n  Target: {remote_dir}")
        for rel_path, content in FILES_TO_SYNC.items():
            remote_path = f"{remote_dir}/{rel_path}"
            try:
                with sftp.file(remote_path, "w") as f:
                    f.write(content)
                print(f"    ✅ {rel_path}")
            except Exception as e:
                print(f"    ❌ {rel_path}: {e}")
        
        # Also write cleaned WSGI
        try:
            wsgi_path = f"{remote_dir}/quickcombo/wsgi.py"
            with sftp.file(wsgi_path, "w") as f:
                f.write(WSGI_CLEAN)
            print(f"    ✅ quickcombo/wsgi.py (clean)")
        except Exception as e:
            print(f"    ❌ wsgi.py: {e}")

    sftp.close()

    # ── STEP 2: Purge ALL Python caches ───────────────────────────────────────
    section("STEP 2: Purging __pycache__ and .pyc files")
    for remote_dir in DIRS:
        cmd = f"find {remote_dir} -type d -name '__pycache__' -exec rm -rf {{}} + 2>/dev/null; find {remote_dir} -name '*.pyc' -delete 2>/dev/null; echo 'Purged {remote_dir}'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(f"    {stdout.read().decode().strip()}")

    # ── STEP 3: Run migrations on quickcombo_app ──────────────────────────────
    section("STEP 3: Running migrations")
    cmd = "cd /home/quickcombo/quickcombo_app && python3 manage.py migrate --run-syncdb 2>&1 | tail -10"
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode().strip())

    # ── STEP 4: Grant admin in quickcombo_app DB ──────────────────────────────
    section(f"STEP 4: Granting admin to {ADMIN_EMAIL}")
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/grant_admin.py', 'w') as f:
        f.write(GRANT_ADMIN_SCRIPT)
    sftp.close()

    stdin, stdout, stderr = ssh.exec_command("python3 /tmp/grant_admin.py 2>&1")
    print(stdout.read().decode().strip())

    # Also SQL update on quickcombo_backend DB (belt AND suspenders)
    sql_cmd = f"sqlite3 /home/quickcombo/www/quickcombo_backend/db.sqlite3 \"UPDATE api_user SET is_staff=1, is_superuser=1 WHERE email='{ADMIN_EMAIL}';\" 2>/dev/null; echo 'SQL done'"
    stdin, stdout, stderr = ssh.exec_command(sql_cmd)
    print(f"  quickcombo_backend DB: {stdout.read().decode().strip()}")

    # ── STEP 5: Hard restart uWSGI ────────────────────────────────────────────
    section("STEP 5: Hard restarting uWSGI")
    ssh.exec_command("killall -9 uwsgi 2>/dev/null || true")
    ssh.exec_command("killall -9 python3 2>/dev/null || true")
    # Touch wsgi.py in BOTH dirs to trigger graceful reload
    for d in DIRS:
        ssh.exec_command(f"touch {d}/quickcombo/wsgi.py")
    print("  Restarted. Waiting 12 seconds...")
    time.sleep(12)

    ssh.close()

    # ── STEP 6: Verify endpoints ──────────────────────────────────────────────
    section("STEP 6: Verifying live endpoints")
    tests = [
        ("https://quickcombo.alwaysdata.net/api/debug-db/", {}),
        ("https://quickcombo.alwaysdata.net/api/admin/stats/", {"X-User-Email": ADMIN_EMAIL}),
        ("https://quickcombo.alwaysdata.net/api/admin/orders/", {"X-User-Email": ADMIN_EMAIL}),
    ]
    all_ok = True
    for url, headers in tests:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            icon = "✅" if r.status_code in (200, 201) else "⚠️ "
            print(f"  {icon} [{r.status_code}] {url}")
            if r.status_code not in (200, 201):
                print(f"       Response: {r.text[:200]}")
                all_ok = False
        except Exception as e:
            print(f"  ❌ {url}: {e}")
            all_ok = False
    
    print()
    if all_ok:
        print("🚀 RESET COMPLETE — All endpoints healthy!")
    else:
        print("⚠️  Some endpoints still failing. Check output above.")

    print(f"\nAdmin Dashboard: https://www.quickcombo.in/admin")
    print(f"Login with: {ADMIN_EMAIL} / admin@4098\n")


if __name__ == "__main__":
    main()
