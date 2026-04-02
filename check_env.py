import paramiko

def check_env():
    print("🚀 Verifying AlwaysData Environment...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=15)
        
        commands = [
            "cd ~/www/quickcombo_backend/",
            "source venv/bin/activate",
            "env | grep DATABASE_URL",
            "cat .env"
        ]
        
        full_cmd = " && ".join(commands)
        stdin, stdout, stderr = ssh.exec_command(full_cmd)
        
        output = stdout.read().decode()
        error = stderr.read().decode()
        
        print("✅ OUTPUT:\n", output)
        if error:
            print("⚠️ ERROR:\n", error)
            
    except Exception as e:
        print("❌ SSH Error:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    check_env()
