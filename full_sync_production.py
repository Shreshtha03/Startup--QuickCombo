import paramiko
import os

def full_sync_production():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    # Sync to BOTH potential live directories to be 100% sure
    REMOTE_ROOTS = [
        "/home/quickcombo/www/quickcombo_backend",
        "/home/quickcombo/quickcombo_app"
    ]
    
    # Files to sync
    files_to_sync = [
        "quickcombo/settings.py",
        "quickcombo/urls.py",
        "api/models.py",
        "api/admin.py",
        "api/views.py",
        "api/admin_views.py",
        "api/serializers.py",
        "api/urls.py",
        "api/migrations/0005_alter_order_status.py"
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Syncing files...")
        
        sftp = ssh.open_sftp()
        for root in REMOTE_ROOTS:
            print(f"\n--- Syncing to {root} ---")
            for f in files_to_sync:
                local_path = f.replace("/", os.sep)
                remote_path = f"{root}/{f}"
                
                # Ensure remote directory exists
                remote_dir = os.path.dirname(remote_path)
                ssh.exec_command(f"mkdir -p {remote_dir}")
                
                print(f"Uploading {f}...")
                sftp.put(local_path, remote_path)
            
            # Clear cache for this root
            print(f"Clearing Python bytecode cache in {root}...")
            ssh.exec_command(f"find {root} -name '__pycache__' -type d -exec rm -rf {{}} +")
            
            # Restart triggers for this root
            ssh.exec_command(f"touch {root}/quickcombo/wsgi.py")

        sftp.close()
        
        # ─── NUCLEAR RESTART ─────────────────────────────────────────────────────────
        print("\n--- Nuclear Restart ---")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("killall -9 python3 || true")
        
        print("\n🚀 Full Production Sync (Multi-Root) Complete!")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    full_sync_production()
