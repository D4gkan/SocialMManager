import unittest

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


if __name__ == "__main__":
    unittest.main()
