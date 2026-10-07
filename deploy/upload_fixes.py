#!/usr/bin/env python3
import os
import sys

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST = "144.31.151.112"
PASSWORD = os.environ["DEPLOY_PASSWORD"]
LOCAL = r"d:\codes\recoveris.io\main"
REMOTE = "/var/www/recoveris.arix.vu/main"

files = [
    "solution-for-individuals/index.html",
    "solution-for-business-vasps/index.html",
    "solution-for-legal-professionals/index.html",
    "solution-for-law-enforcement/index.html",
    "index.html",
    "digital-asset-recovery/index.html",
    "blockchain-investigations/index.html",
    "blockchain-forensic-training/index.html",
    "blockchain-investigation-management-system/index.html",
    "source-of-funds-reports/index.html",
    "aftercare-protocol/index.html",
    "blog/index.html",
    "knowledge-center/index.html",
    "privacy-policy/index.html",
    "terms-and-conditions/index.html",
    "impersonation-recovery-scams-warning/index.html",
]

c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
c.connect(HOST, username="root", password=PASSWORD, timeout=60)
sftp = c.open_sftp()
for rel in files:
    local = f"{LOCAL}\\{rel.replace('/', chr(92))}"
    remote = f"{REMOTE}/{rel}"
    print("put", rel)
    sftp.put(local, remote)
sftp.close()

_, stdout, stderr = c.exec_command(
    r"""
curl -sk --compressed https://recoveris.arix.vu/solution-for-individuals/ | tr '\n' ' ' | grep -oE 'Для .{0,40}лиц|For .{0,20}' | head -5
curl -sk --compressed https://recoveris.arix.vu/ | tr '\n' ' ' | grep -o 'Агентные расследования' | head -1
"""
)
print(stdout.read().decode("utf-8", "replace"))
err = stderr.read().decode("utf-8", "replace")
if err.strip():
    print(err[-500:])
c.close()
print("OK")
