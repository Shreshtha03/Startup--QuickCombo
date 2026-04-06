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

    # Find ALL wsgi.py files and read the WSGI_CONF on alwaysdata
    print("\n[FIND] All wsgi.py files:")
    stdin, stdout, _ = ssh.exec_command("find /home/quickcombo -name 'wsgi.py' 2>/dev/null")
    wsgi_files = stdout.read().decode().strip()
    print(wsgi_files)
    
    for f in wsgi_files.split('\n'):
        f = f.strip()
        if f:
            stdin2, stdout2, _ = ssh.exec_command(f"cat \"{f}\"")
            print(f"\n=== {f} ===")
            print(stdout2.read().decode())

    # Find process config
    print("\n[CONFIG] AlwaysData uWSGI config:")
    stdin3, stdout3, _ = ssh.exec_command("cat /home/quickcombo/etc/uwsgi/*.ini 2>/dev/null || cat /home/quickcombo/.config/alwaysdata/*.json 2>/dev/null || echo 'No config found'")
    print(stdout3.read().decode())
    
    # Also try to find the AlwaysData app config
    stdin4, stdout4, _ = ssh.exec_command("find /home/quickcombo/etc -name '*.ini' -o -name '*.json' 2>/dev/null")
    print("\n[CONFIG FILES]")
    print(stdout4.read().decode())
    
    ssh.close()

if __name__ == "__main__":
    main()
