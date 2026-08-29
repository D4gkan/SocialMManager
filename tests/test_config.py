import os
import tempfile
import unittest
from unittest.mock import patch

import utils
from config import PLATFORMS


class PlatformConfigTests(unittest.TestCase):
    def test_supported_platforms_are_configured(self):
        self.assertEqual(
            list(PLATFORMS.keys()),
            ["instagram", "facebook_business", "tiktok", "x_com"],
        )
        self.assertNotIn("fanvue", PLATFORMS)
        self.assertNotIn("telegram", PLATFORMS)

    def test_facebook_business_link_is_configured(self):
        self.assertIn("facebook_business", PLATFORMS)
        self.assertEqual(
            PLATFORMS["facebook_business"]["url"],
            "https://business.facebook.com/business/loginpage/?next=https%3A%2F%2Fbusiness.facebook.com%2F%3Fnav_ref%3Dbiz_unified_f3_login_page_to_mbs&login_options[0]=FB&login_options[1]=IG&login_options[2]=SSO&config_ref=biz_login_tool_flavor_mbs",
        )
        self.assertEqual(PLATFORMS["facebook_business"]["label"], "Facebook Business")

    def test_x_com_link_is_configured(self):
        self.assertIn("x_com", PLATFORMS)
        self.assertEqual(PLATFORMS["x_com"]["url"], "https://x.com/")
        self.assertEqual(PLATFORMS["x_com"]["label"], "X")


class ProfileDiscoveryTests(unittest.TestCase):
    def test_load_profiles_recovers_existing_profile_dirs(self):
        with tempfile.TemporaryDirectory() as tempdir:
            profiles_dir = os.path.join(tempdir, "profiles")
            profile_name = "Liora"
            os.makedirs(os.path.join(profiles_dir, profile_name), exist_ok=True)
            profiles_file = os.path.join(tempdir, "profiles.json")

            with patch.object(utils, "PROFILES_DIR", profiles_dir), patch.object(
                utils, "PROFILES_FILE", profiles_file
            ):
                profiles = utils.load_profiles()

            self.assertIn(profile_name, profiles)
            self.assertEqual(profiles[profile_name]["profile_path"], os.path.join(profiles_dir, profile_name))


if __name__ == "__main__":
    unittest.main()
