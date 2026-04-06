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

    # Find ALL admin_views files on the server
    print("\n[SEARCH] All admin_views files:")
    stdin, stdout, _ = ssh.exec_command("find /home/quickcombo -name 'admin_views*' 2>/dev/null")
    files_raw = stdout.read().decode().strip()
    print(files_raw)

    # Print the first 5 lines of each .py file
    for f in files_raw.split('\n'):
        f = f.strip()
        if f and f.endswith('.py'):
            stdin2, stdout2, _ = ssh.exec_command(f"head -3 \"{f}\"")
            print(f"\n  {f}:")
            print(stdout2.read().decode())

    # Check the actual api_user table in ALL sqlite databases
    print("\n[DB CHECK] All sqlite files:")
    stdin3, stdout3, _ = ssh.exec_command("find /home/quickcombo -name '*.sqlite3' 2>/dev/null")
    dbs = stdout3.read().decode().strip()
    print(dbs)
    
    for db in dbs.split('\n'):
        db = db.strip()
        if db:
            stdin4, stdout4, _ = ssh.exec_command(
                f"sqlite3 \"{db}\" \"SELECT email,is_staff,is_superuser FROM api_user WHERE email='shreshtha0311@gmail.com';\" 2>/dev/null"
            )
            result = stdout4.read().decode().strip()
            print(f"\n  {db}: {result or '(table not found or empty)'}")

    ssh.close()

if __name__ == "__main__":
    main()
