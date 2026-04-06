import paramiko
import os

def forced_path_alignment():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    HIJACK_ROOT = "/home/quickcombo/quickcombo_app"
    WSGI_PATHS = [
        "/home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py",
        "/home/quickcombo/quickcombo_app/quickcombo/wsgi.py"
    ]
    
    HIJACK_CODE = f"""import sys, os
BASE_DIR = '{HIJACK_ROOT}'
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
# --- ORIGINAL WSGI ---
"""
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Forcing Path Hijack...")
        
        for path in WSGI_PATHS:
            print(f"Hijacking {path}...")
            # We'll prepend the hijack code using sed (using a temp file is safer)
            # Or just rewrite the whole file with a standard WSGI if we know it.
            # Let's read the current content and prepend.
            sftp = ssh.open_sftp()
            try:
                with sftp.file(path, 'r') as f:
                    content = f.read().decode()
                if "import sys, os" not in content[:100]:
                    with sftp.file(path, 'w') as f:
                        f.write(HIJACK_CODE + content)
                    print(f"Proceeded: {path}")
                else:
                    print(f"Already hijacked: {path}")
            except Exception as e:
                print(f"Skipping {path}: {e}")
            sftp.close()
            
        print("\n--- Nuclear Purge & Restart ---")
        ssh.exec_command("find /home/quickcombo/ -name '__pycache__' -type d -exec rm -rf {} +")
        ssh.exec_command("find /home/quickcombo/ -name '*.pyc' -delete")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("killall -9 python3 || true")
        
        print("\n🚀 PATH HIJACK COMPLETE. SITE SHOULD NOW USE /home/quickcombo/quickcombo_app/")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    forced_path_alignment()
