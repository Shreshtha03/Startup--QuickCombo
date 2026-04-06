import paramiko
import os

def find_db():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        # Searching globally for db.sqlite3 files
        cmd = "find /home/quickcombo -name 'db.sqlite3'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        results = stdout.read().decode().strip().split('\n')
        
        print("\n--- DATABASE FILES FOUND ---")
        for db in results:
            if db.strip():
                print(f"📍 {db}")
                # Check for table existence in each
                table_check = f"sqlite3 {db} 'SELECT count(*) FROM api_user;'"
                s_in, s_out, s_err = ssh.exec_command(table_check)
                out = s_out.read().decode().strip()
                err = s_err.read().decode().strip()
                if out:
                    print(f"   ✅ SUCCESS: api_user table exists (Count: {out})")
                else:
                    print(f"   ❌ FAILED: {err or 'Empty output'}")

        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    find_db()
