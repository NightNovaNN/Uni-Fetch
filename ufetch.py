#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import tarfile
import zipfile
from urllib.request import urlopen, Request
import subprocess
import sys

import builder

VERSION = "2.0.0"

# ---------------------------
# Utility
# ---------------------------

def download(url, filename):
    print(f"Downloading: {url}")
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as r:
        with open(filename, "wb") as f:
            shutil.copyfileobj(r, f)
    print(f"Saved to {filename}")

def extract_archive(path, dest):
    print(f"Extracting to: {dest}")
    os.makedirs(dest, exist_ok=True)

    if path.endswith(".zip") or path.endswith(".whl") or path.endswith(".nupkg"):
        with zipfile.ZipFile(path, "r") as z:
            z.extractall(dest)
    else:
        with tarfile.open(path, "r:*") as t:
            t.extractall(dest)

    print("Extraction complete\n")

# ---------------------------
# Fetchers
# ---------------------------

def fetch_github(user_repo, mode="source"):
    print(f"GitHub fetch: {user_repo}")

    user, repo = user_repo.split("/")
    branch = "main"

    if mode == "docs":
        os.makedirs(repo, exist_ok=True)
        readme = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/README.md"
        docs = f"https://api.github.com/repos/{user}/{repo}/contents/docs"

        try:
            download(readme, f"{repo}/README.md")
        except:
            print("README not found")

        try:
            req = Request(docs, headers={"User-Agent": "Mozilla/5.0"})
            data = json.loads(urlopen(req).read().decode())
            if isinstance(data, list):
                os.makedirs(f"{repo}/docs", exist_ok=True)
                for item in data:
                    if item["type"] == "file":
                        url = item["download_url"]
                        name = item["name"]
                        download(url, f"{repo}/docs/{name}")
        except:
            print("docs/ folder not found")

        print("Docs fetch complete\n")
        return

    url = f"https://github.com/{user}/{repo}/archive/refs/heads/{branch}.zip"
    filename = f"{repo}.zip"

    download(url, filename)
    extract_archive(filename, repo)
    os.remove(filename)

def fetch_npm(pkg):
    print(f"npm fetch: {pkg}")

    meta_url = f"https://registry.npmjs.org/{pkg}"
    req = Request(meta_url, headers={"User-Agent": "Mozilla/5.0"})
    meta = json.loads(urlopen(req).read().decode())

    latest = meta["dist-tags"]["latest"]
    tar_url = meta["versions"][latest]["dist"]["tarball"]

    filename = f"{pkg}.tgz"
    folder = f"{pkg}"

    download(tar_url, filename)
    extract_archive(filename, folder)
    os.remove(filename)

def fetch_pypi(pkg):
    print(f"PyPI fetch: {pkg}")

    meta_url = f"https://pypi.org/pypi/{pkg}/json"
    req = Request(meta_url, headers={"User-Agent": "Mozilla/5.0"})
    meta = json.loads(urlopen(req).read().decode())

    if len(meta["urls"]) == 0:
        print("No files found for this PyPI package")
        return

    url = meta["urls"][0]["url"]
    filename = os.path.basename(url)
    folder = pkg

    download(url, filename)
    extract_archive(filename, folder)
    os.remove(filename)

def fetch_choco(pkg):
    print(f"Chocolatey fetch: {pkg}")

    url = f"https://community.chocolatey.org/api/v2/package/{pkg}"
    filename = f"{pkg}.nupkg"
    folder = pkg

    download(url, filename)
    extract_archive(filename, folder)
    os.remove(filename)

# ---------------------------
# Update
# ---------------------------

def self_update():
    print("Self-update is not implemented yet. Future versions will fetch GitHub Releases.")
    print("For now, update manually by replacing ufetch.py or ufetch.exe.\n")

# ---------------------------
# CLI
# ---------------------------

parser = argparse.ArgumentParser(description="UniFetch V2 Universal Fetcher")
parser.add_argument("cmd", help="Command (fetch/build/install/help/version/update)")
parser.add_argument("arg1", nargs="?", help="Main argument")
parser.add_argument("arg2", nargs="?", help="Secondary argument (optional)")

args = parser.parse_args()

cmd = args.cmd
a1 = args.arg1
a2 = args.arg2

# ---------------------------
# Routing
# ---------------------------

if cmd == "help":
    print("""
UniFetch V2 Commands:

Fetch:
  ufetch gh user/repo
  ufetch ghdocs user/repo
  ufetch npm package
  ufetch pypi package
  ufetch choco package

Build:
  ufetch build <file>

Install:
  ufetch install <tool>

Other:
  ufetch update
  ufetch version
  ufetch help
""")

elif cmd == "version":
    print(f"UniFetch version {VERSION}\n")

elif cmd == "update":
    self_update()

elif cmd == "gh":
    fetch_github(a1)

elif cmd == "ghdocs":
    fetch_github(a1, mode="docs")

elif cmd == "npm":
    fetch_npm(a1)

elif cmd == "pypi":
    fetch_pypi(a1)

elif cmd == "choco":
    fetch_choco(a1)

elif cmd == "build":
    builder.build(a1)

else:
    print("Unknown command. Try: ufetch help\n")
