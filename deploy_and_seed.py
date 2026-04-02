import paramiko

def deploy_and_seed():
    print("🚀 Connecting to AlwaysData via SSH...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        # Using credentials found in clean_ssh.py
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=15)
        
        # Commands to pull latest code and run the seed script
        # Commands to pull, restart, and force-seed
        commands = [
            "cd ~/www/quickcombo_backend/",
            "git stash",
            "git pull origin main",
            "touch quickcombo/wsgi.py",  # Forces AlwaysData to reload the Python process
            "sleep 2",
            "curl -X GET https://quickcombo.alwaysdata.net/api/force-seed/"
        ]
        
        full_cmd = " && ".join(commands)
        
        print(f"📡 Executing: {full_cmd}")
        stdin, stdout, stderr = ssh.exec_command(full_cmd)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        if output:
            print("✅ REMOTE OUTPUT:\n", output)
        if error:
            print("⚠️ REMOTE ERROR/WARNING:\n", error)
            
    except Exception as e:
        print("❌ SSH Error:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    deploy_and_seed()
