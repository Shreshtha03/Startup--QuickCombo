import paramiko
import os

def inject_middleware_probes():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    ROOTS = [
        ("/home/quickcombo/www/quickcombo_backend", "WWW"),
        ("/home/quickcombo/quickcombo_app", "APP")
    ]
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected! Injecting Middleware Probes...")
        
        for root, marker in ROOTS:
            # 1. Create api/middleware.py
            mw_path = f"{root}/api/middleware.py"
            mw_content = f"class QCPublicProbeMiddleware:\n    def __init__(self, get_response): self.get_response = get_response\n    def __call__(self, request):\n        response = self.get_response(request)\n        response['X-QC-Source'] = '{marker}'\n        return response\n"
            
            sftp = ssh.open_sftp()
            with sftp.file(mw_path, 'w') as f:
                f.write(mw_content)
            sftp.close()
            print(f"Created {mw_path}")
            
            # 2. Add to settings.py MIDDLEWARE
            # We'll use sed to insert it at the top of MIDDLEWARE list
            settings_path = f"{root}/quickcombo/settings.py"
            cmd = f"sed -i \"/MIDDLEWARE = \\[/,/\\]/ s/MIDDLEWARE = \\[ /MIDDLEWARE = [ 'api.middleware.QCPublicProbeMiddleware', /\" {settings_path}"
            ssh.exec_command(cmd)
            print(f"Added middleware to {settings_path}")
            
        print("\n--- Nuclear Restart ---")
        ssh.exec_command("killall -9 uwsgi || true")
        ssh.exec_command("touch /home/quickcombo/www/quickcombo_backend/quickcombo/wsgi.py")
        ssh.exec_command("touch /home/quickcombo/quickcombo_app/quickcombo/wsgi.py")
        
        print("\n🚀 MIDDLEWARE INJECTED. CHECK HEADERS NOW.")
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    inject_middleware_probes()
