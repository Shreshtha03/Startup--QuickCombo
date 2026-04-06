import paramiko

def force_reload():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Triggering reload...")
        
        # 1. Modify wsgi.py to trigger reload
        ssh.exec_command('echo " " >> ~/www/quickcombo_backend/quickcombo/wsgi.py')
        
        # 2. Kill uWSGI to force a fresh process
        stdin, stdout, stderr = ssh.exec_command('killall -9 uwsgi')
        print(stdout.read().decode())
        print(stderr.read().decode())
        
        # 3. Check uptime or logs
        print("🚀 Forced Reload complete. Waiting for uWSGI to spawn...")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    force_reload()
