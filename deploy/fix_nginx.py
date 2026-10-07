import os
import sys

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

NGINX = """# Isolated site for recoveris.arix.vu — do not reuse for other projects
server {
    server_name recoveris.arix.vu;

    location / {
        proxy_pass http://127.0.0.1:3011;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen [::]:443 ssl;
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/recoveris.arix.vu/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/recoveris.arix.vu/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = recoveris.arix.vu) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    listen [::]:80;
    server_name recoveris.arix.vu;
    return 404;
}
"""

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(
    "144.31.151.112",
    username="root",
    password=os.environ["DEPLOY_PASSWORD"],
    timeout=30,
)

sftp = c.open_sftp()
with sftp.file("/etc/nginx/sites-available/recoveris.arix.vu", "w") as f:
    f.write(NGINX)
with sftp.file(
    "/var/www/recoveris.arix.vu/deploy/nginx.recoveris.arix.vu.conf", "w"
) as f:
    f.write(NGINX)
sftp.close()

script = r"""
set -e
ln -sfn /etc/nginx/sites-available/recoveris.arix.vu /etc/nginx/sites-enabled/recoveris.arix.vu
nginx -t
systemctl reload nginx
echo FIXED
curl -skI https://127.0.0.1/individuals -H 'Host: recoveris.arix.vu' | head -12
curl -skI https://recoveris.arix.vu/business | head -8
curl -skI https://recoveris.arix.vu/contact | head -8
curl -sk https://recoveris.arix.vu/individuals | tr '\n' ' ' | grep -o 'частных лиц' | head -1
"""

_, stdout, stderr = c.exec_command(script)
print(stdout.read().decode("utf-8", errors="replace"))
err = stderr.read().decode("utf-8", errors="replace")
if err.strip():
    print("ERR", err[-1500:])
c.close()
