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
python3 - <<'PY'
import urllib.request, ssl
ctx = ssl._create_unverified_context()
paths = [
  "/", "/individuals", "/business", "/legal", "/law-enforcement",
  "/investigations", "/recovery", "/source-of-funds", "/aftercare",
  "/training", "/bims", "/blog", "/knowledge-center", "/contact",
  "/terms", "/privacy", "/scam-warning",
]
for p in paths:
  try:
    req = urllib.request.Request("https://recoveris.arix.vu"+p, method="GET")
    with urllib.request.urlopen(req, context=ctx, timeout=20) as r:
      body = r.read(2000).decode("utf-8", "replace")
      print(r.status, p, "ru" if 'lang="ru"' in body or "част" in body or "Recoveris" in body else "")
  except Exception as e:
    print("ERR", p, e)
PY
"""

_, stdout, stderr = c.exec_command(script)
print(stdout.read().decode("utf-8", errors="replace"))
print(stderr.read().decode("utf-8", errors="replace")[-500:])
c.close()
