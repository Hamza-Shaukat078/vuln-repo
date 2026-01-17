# vuln_cmd_injection.py
# Vulnerability: OS Command Injection (OWASP A03 Injection)

import os

def ping_host(host):
    # ❌ Vulnerable: user-controlled string goes directly into shell command
    cmd = f"ping -c 1 {host}"
    print("[DEBUG] Executing:", cmd)
    os.system(cmd)

if __name__ == "__main__":
    host = input("Enter host to ping: ")
    ping_host(host)
