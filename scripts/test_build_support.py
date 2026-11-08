import json, os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
HELP = os.environ.get("HELP_JSON", os.path.expanduser(
    "~/CodingProjects/aisleledger-wt/android/shared/help/help.json"))


class BuildSupportTests(unittest.TestCase):
    def setUp(self):
        import build_support
        self.help = json.load(open(HELP))
        self.html = build_support.render(self.help)

    def test_every_faq_and_feature_title_appears(self):
        import html
        for item in self.help["faq"]:
            self.assertIn(html.escape(item["q"]), self.html)
        for item in self.help["features"]:
            self.assertIn(html.escape(item["title"]), self.html)

    def test_both_platform_cancel_steps_appear(self):
        self.assertIn("Play Store", self.html)
        self.assertIn("tap your name", self.html)
        self.assertIn("iPhone", self.html)
        self.assertIn("Android", self.html)

    def test_contact_email_present(self):
        self.assertIn("mailto:support@gigledger.org", self.html)

    def test_html_escapes(self):
        import build_support
        page = build_support.render({**self.help, "faq": [{"q": "Tom & Jerry <b>", "a": "x"}]})
        self.assertIn("Tom &amp; Jerry &lt;b&gt;", page)


if __name__ == "__main__":
    unittest.main()
