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
for u in / /individuals /business /legal /law-enforcement /investigations /recovery /source-of-funds /aftercare /training /bims /blog /knowledge-center /contact /terms /privacy /scam-warning /blog/swiss-10-5m-recovery; do
  code=$(curl -sk -o /dev/null -w '%{http_code}' "https://recoveris.arix.vu$u")
  echo "$code $u"
done
echo '=== FONT ==='
curl -sk https://recoveris.arix.vu/ | grep -oE 'Manrope|font-sans|cyrillic' | sort -u | head
echo '=== HOME RICH ==='
curl -sk https://recoveris.arix.vu/ | tr '\n' ' ' | grep -oE 'Агентные расследования|Кому помогаем|ZondaCrypto|Upbit' | sort -u
echo '=== BUSINESS RICH ==='
curl -sk https://recoveris.arix.vu/business | tr '\n' ' ' | grep -oE 'Для бизнеса|BIMS|Aftercare Protocol|Source of Funds' | sort -u
echo '=== BLOG ITEMS ==='
curl -sk https://recoveris.arix.vu/blog | grep -c 'services-item' || true
"""

_, stdout, stderr = c.exec_command(script)
print(stdout.read().decode("utf-8", errors="replace"))
err = stderr.read().decode("utf-8", errors="replace")
if err.strip():
    print("ERR", err[:500])
c.close()
