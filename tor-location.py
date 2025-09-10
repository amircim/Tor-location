#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
import requests
import sys

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

    # بستن هر تور قبلی با همین کانفیگ
    subprocess.run(f"pkill -f 'tor -f {torrc_path}'", shell=True)

    # اجرای تور
    subprocess.Popen(f"tor -f {torrc_path}", shell=True)
    print(f"[*] Starting Tor for {country_code} on port {TOR_PORT}...")
    time.sleep(20)  # صبر تا تور کانکشن بسازه

    print(f"[+] Tor {country_code} started, IP: {ma_ip(TOR_PORT)}")

if __name__ == "__main__":
    os.system("clear")
    country = input("Enter country code (e.g. FR, DE, US): ").strip().upper()
    if not country:
        print("[-] No country code entered!")
        sys.exit(1)

    start_tor(country)