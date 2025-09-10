
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import requests
import sys
import time

TOR_BASE_DIR = "/root/tor-single"
TOR_PORT = 9054

def ma_ip(port):
    url = "http://checkip.amazonaws.com"
    proxies = {"http": f"socks5://127.0.0.1:{port}", "https": f"socks5://127.0.0.1:{port}"}
    try:
        r = requests.get(url, proxies=proxies, timeout=10)
        return r.text.strip()
    except:
        return "Cannot connect"

def start_tor(country_code):
    data_dir = os.path.join(TOR_BASE_DIR, country_code)
    torrc_path = os.path.join(data_dir, f"torrc-{country_code}.conf")

    os.makedirs(data_dir, exist_ok=True)

    if not os.path.isfile(torrc_path):
        with open(torrc_path, "w") as f:
            f.write(f"SocksPort {TOR_PORT}\n")
            f.write(f"DataDirectory {data_dir}\n")
            f.write(f"ExitNodes {{{country_code}}}\n")
            f.write("StrictNodes 1\n")
            f.write("Log notice stdout\n")

    # بستن هر تور قبلی با همین کانفیگ
    subprocess.run(f"pkill -f 'tor -f {torrc_path}'", shell=True)

    # اجرای تور و گرفتن لاگ
    proc = subprocess.Popen(f"tor -f {torrc_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    print(f"[*] Starting Tor for {country_code} on port {TOR_PORT}...")

    # صبر تا Bootstrapped 100%
    while True:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        print(line.strip())
        if "Bootstrapped 100%" in line:
            break

    print(f"[+] Tor {country_code} ready, IP: {ma_ip(TOR_PORT)}")
    return proc

if __name__ == "__main__":
    os.system("clear")
    country = input("Enter country code (e.g. FR, DE, US): ").strip().upper()
    if not country:
        print("[-] No country code entered!")
        sys.exit(1)

    tor_proc = start_tor(country)

    input("[*] Press Enter to stop Tor...")
    tor_proc.terminate()
    print("[+] Tor stopped.")