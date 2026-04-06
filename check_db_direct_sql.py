import paramiko

def check_db_direct_sql():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    DB_FILE = "/home/quickcombo/www/quickcombo_backend/db.sqlite3"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        cmd = f"sqlite3 {DB_FILE} \".headers on\" \".mode column\" \"SELECT * FROM api_user;\""
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print("\n--- ALL USERS ---")
        print(stdout.read().decode())
            
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_db_direct_sql()
