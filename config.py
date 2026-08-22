"""
Configuration for the Multi-Account Session Manager.

Only paths and URLs live here — no credentials, and no anti-detection
settings (custom user-agents, automation flags, fingerprinting). See the
top of main.py for why those are left out.
"""

import os

# --- Chrome executable candidates (Windows) ---
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]

# --- The links every profile opens ---
PLATFORMS = {
    "instagram": {"label": "Instagram", "url": "https://www.instagram.com/"},
    "facebook_business": {
        "label": "Facebook Business",
        "url": "https://business.facebook.com/business/loginpage/?next=https%3A%2F%2Fbusiness.facebook.com%2F%3Fnav_ref%3Dbiz_unified_f3_login_page_to_mbs&login_options[0]=FB&login_options[1]=IG&login_options[2]=SSO&config_ref=biz_login_tool_flavor_mbs",
    },
    "tiktok": {"label": "TikTok", "url": "https://www.tiktok.com/"},
    "x_com": {"label": "X", "url": "https://x.com/"},
}

# --- Project paths ---
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(PROJECT_DIR, "profiles")
PROFILES_FILE = os.path.join(PROJECT_DIR, "profiles.json")

MIN_PYTHON = (3, 10)
