"""
The user IS staff in the DB, but we're still getting 403.
This means the LIVE server is NOT loading the updated admin_views.py code.
It's loading CACHED bytecode from __pycache__ that has old logic.

Solution: 
1. Wipe __pycache__ on the server
2. Touch wsgi.py in the exact live dir
3. Let it restart naturally
"""
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

    live_root = "/home/quickcombo/quickcombo_app"
    backend_root = "/home/quickcombo/www/quickcombo_backend"

    # 1. Nuclear cache purge
    print("\n[PURGE] Nuking all .pyc and __pycache__ ...")
    cmds = [
        f"find {live_root} -name '*.pyc' -delete",
        f"find {live_root} -type d -name '__pycache__' -exec rm -rf {{}} + 2>/dev/null || true",
        f"find {backend_root} -name '*.pyc' -delete",
        f"find {backend_root} -type d -name '__pycache__' -exec rm -rf {{}} + 2>/dev/null || true",
        "find /home/quickcombo -name '*.pyc' -delete 2>/dev/null || true",
    ]
    for cmd in cmds:
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdout.read()  # drain
    print("    Done.")

    # 2. Kill all uwsgi and python3
    print("\n[RESTART] Killing uWSGI + Python processes...")
    ssh.exec_command("killall -9 uwsgi 2>/dev/null || true")
    ssh.exec_command("killall -9 python3 2>/dev/null || true")
    time.sleep(2)
    
    # 3. Touch wsgi.py in the backend (the one that actually gets served)
    ssh.exec_command(f"touch {backend_root}/quickcombo/wsgi.py")
    ssh.exec_command(f"touch {live_root}/quickcombo/wsgi.py")
    print("    Touched wsgi.py files. Waiting 15 seconds for uWSGI to reload...")
    
    ssh.close()
    time.sleep(15)

    # 4. Test
    print("\n[TEST] Checking admin endpoint...")
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'},
        timeout=25
    )
    print(f"  Status: {r.status_code}")
    print(f"  Body: {r.text[:300]}")
    
    if r.status_code == 200:
        print("\n✅ SUCCESS! Admin dashboard is LIVE!")
    elif r.status_code == 403:
        print("\n❌ Still 403 — the server is loading cached admin_views with different logic.")
        print("   Need to check what VERSION of admin_views is running remotely.")
    elif r.status_code == 401:
        print("\n⚠️  Got 401 — server can't find the user in DB. DB mismatch issue.")
    else:
        print(f"\n❓ Unexpected: {r.status_code}")

if __name__ == "__main__":
    main()
