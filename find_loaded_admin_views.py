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

    # 1. Find ALL admin_views.py and their .pyc counterparts
    print("\n[SEARCH] All admin_views files:")
    stdin, stdout, _ = ssh.exec_command("find /home/quickcombo -name 'admin_views*' 2>/dev/null")
    files = stdout.read().decode().strip()
    print(files)
    
    # 2. Show content of each one
    for f in files.split('\n'):
        f = f.strip()
        if f and f.endswith('.py') and not f.endswith('.pyc'):
            stdin2, stdout2, _ = ssh.exec_command(f"head -5 '{f}'")
            print(f"\n--- {f} ---")
            print(stdout2.read().decode())

    # 3. Remove ALL .pyc of admin_views
    print("\n[DELETE] Removing all admin_views .pyc...")
    stdin3, stdout3, _ = ssh.exec_command("find /home/quickcombo -name 'admin_views*.pyc' -delete -print 2>/dev/null")
    deleted = stdout3.read().decode().strip()
    print(f"Deleted: {deleted or '(none found)'}")

    # 4. Show what code will be loaded by checking sys.path order
    check_script = """
import sys
sys.path.insert(0, '/home/quickcombo/quickcombo_app')
import importlib.util
import api.admin_views as av
print('Loaded from:', av.__file__)
print('admin_stats is:', av.admin_stats)
"""
    sftp = ssh.open_sftp()
    with sftp.file('/tmp/check_load.py', 'w') as f:
        f.write(check_script)
    sftp.close()
    
    stdin4, stdout4, stderr4 = ssh.exec_command(
        "cd /home/quickcombo/quickcombo_app && DJANGO_SETTINGS_MODULE=quickcombo.settings python3 /tmp/check_load.py 2>&1"
    )
    print("\n[LOAD CHECK]")
    print(stdout4.read().decode())
    
    ssh.close()

    # 5. Test
    print("\n[TEST]")
    r = requests.get(
        'https://quickcombo.alwaysdata.net/api/admin/stats/',
        headers={'X-User-Email': 'shreshtha0311@gmail.com'},
        timeout=20
    )
    print(f"  {r.status_code}: {r.text[:300]}")

if __name__ == "__main__":
    main()
