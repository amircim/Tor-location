#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import time
import requests
import socks
import socket

TOR_BASE_DIR = "/root/tor-test"
TOR_PORT = 9054

def create_tor_instance(country_code):
    data_dir = os.path.join(TOR_BASE_DIR, country_code)
    torrc_path = f"/tmp/torrc-{country_code}.conf"

    os.makedirs(data_dir, exist_ok=True)

    torrc_content = f"""
SocksPort {TOR_PORT}
DataDirectory {data_dir}
ExitNodes {{{country_code}}}
StrictNodes 1
Log notice stdout
"""
    with open(torrc_path, "w") as f:
        f.write(torrc_content.strip())

    print(f"[+] Starting Tor with exit node {country_code} on port {TOR_PORT} ...")
    proc = subprocess.Popen(["tor", "-f", torrc_path])
    return proc

def get_ip_via_tor():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", TOR_PORT)
    socket.socket = socks.socksocket
    try:
        ip = requests.get("https://api.ipify.org", timeout=10).text
        return ip
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    code = input("Enter country code (e.g. FR, DE, US): ").strip().upper()
    proc = create_tor_instance(code)

    print("[*] Waiting for Tor to establish circuit...")
    time.sleep(20)  # صبر می‌کنیم تا تور کامل وصل بشه

    ip = get_ip_via_tor()
    print(f"[+] Your Tor exit IP for {code}: {ip}")

    # اگر بخوای تور رو بعد تست ببندی:
    # proc.terminate()