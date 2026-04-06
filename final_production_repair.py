import paramiko
import os

def final_production_repair():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    # THE ACTUAL LIVE DIRECTORY (CONTAINING .GIT)
    LIVE_ROOT = "/home/quickcombo/quickcombo_app"
    LOCAL_BASE = r"c:\Placement project\Quickcombo"
    
    files_to_force_sync = [
        "quickcombo/settings.py",
        "quickcombo/urls.py",
        "api/models.py",
        "api/admin.py",
        "api/views.py",
        "api/admin_views.py",
        "api/serializers.py",
        "api/urls.py",
    ]
    
    print(f"Connecting to {host} as {user}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Starting Nuclear Repair...")
        
        sftp = ssh.open_sftp()
        for f in files_to_force_sync:
            local_path = os.path.join(LOCAL_BASE, f.replace("/", os.sep))
            remote_path = f"{LIVE_ROOT}/{f}"
            
            if not os.path.exists(local_path):
                print(f"⚠️ Local file MISSING: {local_path}")
                continue
                
            remote_dir = os.path.dirname(remote_path)
            ssh.exec_command(f"mkdir -p {remote_dir}")
            
            print(f"Uploading {f}...")
            sftp.put(local_path, remote_path)
            
            # Verify
            stdin, stdout, stderr = ssh.exec_command(f"ls -l {remote_path}")
            print(f"✅ Verified: {stdout.read().decode().strip()}")
            
        sftp.close()
        
        print("\n--- Purging All __pycache__ on Server ---")
        ssh.exec_command("find /home/quickcombo/ -name '__pycache__' -type d -exec rm -rf {} +")
        
        print("\n--- Nuclear Restart ---")
        ssh.exec_command(f"touch {LIVE_ROOT}/quickcombo/wsgi.py")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("killall -9 python3 || true")
        
        print("\n🚀 NUCLEAR REPAIR COMPLETE!")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    final_production_repair()
