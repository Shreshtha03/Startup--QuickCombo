import paramiko
import os

def check_remote_email():
    host = "ssh-quickcombo.alwaysdata.net"
    user = "quickcombo"
    password = "Dinesh@061004"
    
    print(f"Connecting to {host}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(host, username=user, password=password)
        print("Connected!")
        
        test_script = """
import os
import sys
import django

sys.path.insert(0, '/home/quickcombo/quickcombo_app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'quickcombo.settings'
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', False)}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

try:
    print("Attempting to send test email to shreshtha0311@gmail.com...")
    result = send_mail(
        'QuickCombo Production Email Test',
        'If you are reading this, the Django SMTP configuration on AlwaysData is working perfectly.',
        getattr(settings, 'DEFAULT_FROM_EMAIL', 'support@quickcombo.in'),
        ['shreshtha0311@gmail.com'],
        fail_silently=False,
    )
    print(f"SUCCESS: Result = {result}")
except Exception as e:
    print(f"ERROR: {e}")
"""
        sftp = ssh.open_sftp()
        with sftp.file('/tmp/test_remote_email.py', 'w') as f:
            f.write(test_script)
        sftp.close()
        
        print("\nExecuting test...")
        stdin, stdout, stderr = ssh.exec_command("python3 /tmp/test_remote_email.py 2>&1")
        print(stdout.read().decode())
        
        ssh.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_remote_email()
