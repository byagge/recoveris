#!/usr/bin/env python3
"""Deploy main/ static mirror to recoveris.arix.vu and switch nginx to static root."""
from __future__ import annotations

import os
import sys
import tarfile
import tempfile
from pathlib import Path

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HOST = "144.31.151.112"
USER = "root"
REMOTE_ROOT = "/var/www/recoveris.arix.vu"
LOCAL_MAIN = Path(r"d:\codes\recoveris.io\main")
LOCAL_NGINX = Path(r"d:\codes\recoveris.io\deploy\nginx.recoveris.arix.vu.conf")

NGINX = LOCAL_NGINX.read_text(encoding="utf-8")

password = os.environ.get("DEPLOY_PASSWORD")
if not password:
    sys.exit("Set DEPLOY_PASSWORD env var")


def main() -> None:
    print("Packing main/ ...")
    tmp = Path(tempfile.gettempdir()) / "recoveris-main.tar.gz"
    with tarfile.open(tmp, "w:gz") as tar:
        tar.add(LOCAL_MAIN, arcname="main")
    size_mb = tmp.stat().st_size / (1024 * 1024)
    print(f"Archive: {tmp} ({size_mb:.1f} MB)")

    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting {HOST} ...")
    c.connect(HOST, username=USER, password=password, timeout=60)

    def run(cmd: str, timeout: int = 300) -> str:
        print(f"$ {cmd}")
        _, stdout, stderr = c.exec_command(cmd, timeout=timeout)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        code = stdout.channel.recv_exit_status()
        if out.strip():
            print(out[-3000:])
        if err.strip():
            print("ERR:", err[-2000:])
        if code != 0:
            raise RuntimeError(f"Command failed ({code}): {cmd}")
        return out

    run(f"mkdir -p {REMOTE_ROOT}/deploy {REMOTE_ROOT}/main")

    print("Uploading archive via SFTP ...")
    sftp = c.open_sftp()
    remote_tar = f"{REMOTE_ROOT}/recoveris-main.tar.gz"
    sftp.put(str(tmp), remote_tar)

    with sftp.file(f"{REMOTE_ROOT}/deploy/nginx.recoveris.arix.vu.conf", "w") as f:
        f.write(NGINX)
    with sftp.file("/etc/nginx/sites-available/recoveris.arix.vu", "w") as f:
        f.write(NGINX)
    sftp.close()

    run(
        f"""
set -e
cd {REMOTE_ROOT}
# replace main atomically
rm -rf main.prev
if [ -d main ]; then mv main main.prev; fi
tar -xzf recoveris-main.tar.gz
rm -f recoveris-main.tar.gz
# stop Next.js app if running — site is now static
pm2 stop recoveris 2>/dev/null || true
pm2 delete recoveris 2>/dev/null || true
ln -sfn /etc/nginx/sites-available/recoveris.arix.vu /etc/nginx/sites-enabled/recoveris.arix.vu
nginx -t
systemctl reload nginx
echo PAGES=$(find main -name index.html | wc -l)
echo IMAGES=$(find main/images -type f | wc -l)
curl -skI https://127.0.0.1/ -H 'Host: recoveris.arix.vu' | head -15
curl -skI https://127.0.0.1/solution-for-individuals/ -H 'Host: recoveris.arix.vu' | head -10
curl -sk https://127.0.0.1/solution-for-individuals/ -H 'Host: recoveris.arix.vu' | tr '\\n' ' ' | grep -o 'For Individuals' | head -1
curl -skI https://recoveris.arix.vu/ | head -10
""",
        timeout=600,
    )

    c.close()
    print("DEPLOY OK")


if __name__ == "__main__":
    main()
