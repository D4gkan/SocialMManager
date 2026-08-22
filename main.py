"""
Multi-Account Session Manager — CLI entry point.

WHAT THIS DOES
    Each profile is its own Chrome --user-data-dir. Launching a profile
    opens one Chrome window with tabs for Instagram, Facebook Business,
    TikTok, and X, all sharing that profile's cookies. Log into each site
    by hand the first time; later launches auto-login to those four. No
    passwords are stored or handled here.

WHAT THIS DOES NOT DO
    It does not spoof user-agents, disable Chrome's automation-detection
    flags, randomize fingerprints, or otherwise try to help a profile dodge
    a platform's own fraud/bot-detection checks. Chrome behaves exactly as
    it would if opened by hand.
"""

import os
import sys

from config import PROFILES_DIR
import utils

MENU = """
+-------------------------------------------+
| Multi-Account Session Manager             |
+-------------------------------------------+
| 1. Create Profile                         |
| 2. Launch Profile                         |
| 3. List Profiles                          |
| 4. Delete Profile                         |
| 5. Check System Status                    |
| 6. Exit                                  |
+-------------------------------------------+
"""


def menu_create():
    name = input("Profile name (alphanumeric only): ").strip()
    utils.create_profile(name)


def menu_launch():
    profiles = utils.get_valid_profiles(utils.load_profiles())
    if not profiles:
        print("No profiles yet. Create one first.")
        return

    names = sorted(profiles.keys())
    print("\nProfiles:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")

    choice = input("Select profile (number): ").strip()
    try:
        selected = names[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    utils.launch_profile(profiles[selected]["profile_path"])


def menu_delete():
    profiles = utils.get_valid_profiles(utils.load_profiles())
    if not profiles:
        print("No profiles to delete.")
        return

    names = sorted(profiles.keys())
    print("\nProfiles:")
    for i, name in enumerate(names, 1):
        print(f"  {i}. {name}")

    choice = input("Select profile to delete (number): ").strip()
    try:
        selected = names[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    utils.delete_profile(selected)


def main():
    os.makedirs(PROFILES_DIR, exist_ok=True)

    actions = {
        "1": menu_create,
        "2": menu_launch,
        "3": utils.list_profiles,
        "4": menu_delete,
        "5": utils.check_system_status,
    }

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()
        if choice == "6":
            print("Goodbye.")
            sys.exit(0)
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
