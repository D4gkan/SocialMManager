"""
Core helpers for the Multi-Account Session Manager.

Each profile is a single Chrome --user-data-dir. Launching a profile opens
Chrome with a tab for each of the supported platforms (Instagram, Facebook
Business, TikTok, and X), all sharing that one profile's cookies. Log into
each site once inside a profile and future launches auto-login to those four.

launch_profile() only ever opens a normal, visible Chrome window. It does
not set a custom user-agent, flip any of Chrome's automation-detection
flags, or randomize a fingerprint.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime

from config import CHROME_PATHS, MIN_PYTHON, PLATFORMS, PROFILES_DIR, PROFILES_FILE

NAME_RE = re.compile(r"^[A-Za-z0-9]+$")


# ---------- profiles.json ----------

def load_profiles():
    if not os.path.exists(PROFILES_FILE):
        return {}
    with open(PROFILES_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("profiles.json is corrupted or empty — starting fresh.")
            return {}


def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=2)


# ---------- profile lifecycle ----------

def create_profile(name):
    if not NAME_RE.match(name or ""):
        print("Profile name must be alphanumeric only (letters and numbers, no spaces).")
        return False

    profiles = load_profiles()
    if name in profiles:
        print(f"Profile '{name}' already exists.")
        return False

    profile_path = os.path.join(PROFILES_DIR, name)
    os.makedirs(profile_path, exist_ok=True)

    profiles[name] = {
        "profile_path": profile_path,
        "created": datetime.now().isoformat(timespec="seconds"),
    }
    save_profiles(profiles)
    print(f"Created profile '{name}' -> {profile_path}")
    print("Launching it will open Instagram, Facebook Business, TikTok, and X together.")
    return True


def delete_profile(name):
    profiles = load_profiles()
    if name not in profiles:
        print(f"Profile '{name}' not found.")
        return False

    confirm = input(
        f"Delete '{name}' and its profile data? This cannot be undone. (y/n): "
    ).strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return False

    profile_path = profiles[name].get("profile_path", "")
    if profile_path and os.path.isdir(profile_path):
        shutil.rmtree(profile_path, ignore_errors=True)

    del profiles[name]
    save_profiles(profiles)
    print(f"Deleted profile '{name}'.")
    return True


def get_valid_profiles(profiles):
    """Only profiles whose directory still exists on disk."""
    return {
        name: data
        for name, data in profiles.items()
        if os.path.isdir(data.get("profile_path", ""))
    }


def list_profiles():
    profiles = get_valid_profiles(load_profiles())
    if not profiles:
        print("No profiles yet. Use 'Create Profile' first.")
        return

    links = ", ".join(p["label"] for p in PLATFORMS.values())
    print("\nProfile launcher")
    print("-" * 28)
    print(f"Each profile opens: {links}")
    print("-" * 28)
    for name in sorted(profiles):
        print(f"  • {name}  | created {profiles[name]['created']}")
    print()


# ---------- Chrome ----------

def get_chrome_executable():
    for path in CHROME_PATHS:
        if path and os.path.isfile(path):
            return path
    return shutil.which("chrome") or shutil.which("chrome.exe")


def launch_profile(profile_path):
    """
    Open one Chrome window on profile_path with a tab for each of the
    supported platforms. Nothing else is modified: no user-agent override,
    no automation flags, no fingerprint changes — it behaves exactly like
    opening Chrome on that profile and clicking bookmarked tabs.
    """
    chrome_path = get_chrome_executable()
    if not chrome_path:
        print("Could not find chrome.exe. Check CHROME_PATHS in config.py.")
        return False

    urls = [p["url"] for p in PLATFORMS.values()]
    subprocess.Popen([chrome_path, f"--user-data-dir={profile_path}", *urls])
    print("Launching Chrome with Instagram, Facebook Business, TikTok, and X...")
    return True


# ---------- system checks ----------

def validate_python_version():
    return sys.version_info >= MIN_PYTHON


def check_system_status():
    print("\nSystem Status")
    print("-" * 24)
    print(f"Python {sys.version.split()[0]}: "
          f"{'OK' if validate_python_version() else 'Needs 3.10+'}")

    chrome_path = get_chrome_executable()
    print(f"Chrome: {'Found at ' + chrome_path if chrome_path else 'NOT FOUND'}")

    print(f"profiles.json: {'Found' if os.path.exists(PROFILES_FILE) else 'Not created yet'}")

    profiles = get_valid_profiles(load_profiles())
    print(f"Profiles: {len(profiles)}")
    print(f"Links per profile: {', '.join(p['label'] for p in PLATFORMS.values())}")
    print()
