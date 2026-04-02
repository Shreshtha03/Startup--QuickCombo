import paramiko

def run():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('ssh-quickcombo.alwaysdata.net', username='quickcombo', password='Dinesh@061004', timeout=10)
        
        cmd = "cat ~/admin/logs/sites/quickcombo.alwaysdata.net/apache.log* ~/admin/logs/sites/quickcombo.alwaysdata.net/error.log* ~/admin/logs/uwsgi/quickcombo*.log | tail -n 100"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        
        print("OUT:", stdout.read().decode())
        print("ERR:", stderr.read().decode())
            
    except Exception as e:
        print("SSH Error:", e)
    finally:
        ssh.close()

if __name__ == "__main__":
    run()
