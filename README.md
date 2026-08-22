# Multi-Account Session Manager

A CLI tool for keeping isolated Chrome sessions for accounts you personally
run across Instagram, Facebook Business, TikTok, and X — logging into one
doesn't touch the others, and cookies persist so you don't re-login every
time.

## What's different from the original spec

This leaves out the anti-detection layer: custom user-agent spoofing,
disabling Chrome's automation flags, and randomized browser fingerprinting.
These are built specifically to help an account avoid a platform's own
fraud/bot detection, so they're not included here.

That layer also isn't needed for what this tool actually does. Chrome is
launched normally, pointed at a profile folder — the same as opening the
browser and clicking into a saved profile by hand. A real person logging in
through a real browser has nothing to hide from these sites in the first
place.

## Setup

1. Python 3.10+ and Google Chrome installed on Windows.
2. No extra packages — everything here is the standard library.
3. Double-click `start.bat`, or run `python main.py` from this folder.

## Using it

- **Create Account** — pick a platform and a name; creates an empty Chrome
  profile folder under `profiles/`.
- **Launch Account** — opens Chrome at that platform's URL using that
  profile. Log in by hand the first time; Chrome keeps the cookies for next
  time.
- **List / Delete / Status** — manage what's already set up.

## Files

- `config.py` — Chrome paths, platform URLs, project paths.
- `utils.py` — account storage (`accounts.json`), Chrome launching, system checks.
- `main.py` — the CLI menu.
- `start.bat` — double-click entry point.

`accounts.json` only ever stores platform, profile path, and creation
timestamp — never credentials.
