import os
import sys

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(
    "144.31.151.112",
    username="root",
    password=os.environ["DEPLOY_PASSWORD"],
    timeout=30,
)

script = r"""
set -e
echo '=== NGINX CONFIG ==='
cat /etc/nginx/sites-enabled/recoveris.arix.vu
echo '=== LOCAL HTTPS via Host ==='
curl -skI https://127.0.0.1/individuals -H 'Host: recoveris.arix.vu' | head -15
echo '=== PUBLIC ==='
curl -skI https://recoveris.arix.vu/individuals | head -15
curl -skI https://recoveris.arix.vu/business | head -8
curl -skI https://recoveris.arix.vu/contact | head -8
echo '=== BODY SNIP ==='
curl -sk https://recoveris.arix.vu/ | tr '\n' ' ' | grep -o 'lang="ru"' | head -1
curl -sk https://recoveris.arix.vu/individuals | tr '\n' ' ' | grep -o 'частных лиц' | head -1
"""

_, stdout, stderr = c.exec_command(script)
print(stdout.read().decode("utf-8", errors="replace"))
err = stderr.read().decode("utf-8", errors="replace")
if err.strip():
    print("ERR", err[:1000])
c.close()
