from django.test import TestCase
from .models import SiteInfo


class SiteInfoTest(TestCase):
    def test_create_siteinfo(self):
        site = SiteInfo.objects.create(
            site_name="Test Site",
            site_number="123456789",
            site_email="test@example.com",
            site_description="A test description",
            site_slogan="Just testing",
            copyright_text="© 2024 Test",
        )
        self.assertEqual(str(site), "Test Site")
        self.assertEqual(site.site_email, "test@example.com")