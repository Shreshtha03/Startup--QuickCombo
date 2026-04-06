import paramiko
import os

def final_sql_grant():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    DB_FILE = "/home/quickcombo/www/quickcombo_backend/db.sqlite3"
    email = "shreshtha0311@gmail.com"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        # SQL Command targeting the PROVEN database file
        sql = f"UPDATE api_user SET is_staff=1, is_superuser=1 WHERE email='{email}';"
        cmd = f"sqlite3 {DB_FILE} \"{sql}\""
        
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print("✅ SQL UPDATE ATTEMPTED.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    final_sql_grant()
