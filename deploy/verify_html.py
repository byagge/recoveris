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
import urllib.request, ssl, re
ctx = ssl._create_unverified_context()
home = urllib.request.urlopen('https://recoveris.arix.vu/', context=ctx).read().decode('utf-8','replace')
blog = urllib.request.urlopen('https://recoveris.arix.vu/blog', context=ctx).read().decode('utf-8','replace')
print('HOME_LEN', len(home))
print('FONT_CLASSES', sorted(set(re.findall(r'class="[^"]*font[^"]*"', home)))[:5])
print('MANROPE', 'Manrope' in home, 'manrope' in home.lower())
print('HAS_CYR', 'Агентные' in home)
print('BLOG_LEN', len(blog))
print('BLOG_READ', blog.count('Читать'))
print('BLOG_TITLES', len(re.findall(r'<h3>', blog)))
print('SAMPLE_TITLES', re.findall(r'<h3>(.*?)</h3>', blog)[:3])
PY
"""

_, stdout, stderr = c.exec_command(script)
print(stdout.read().decode("utf-8", errors="replace"))
err = stderr.read().decode("utf-8", errors="replace")
if err.strip():
    print("ERR", err[:800])
c.close()
