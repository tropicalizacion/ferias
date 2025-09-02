from django.test import TestCase
from wagtail.models import Page

from .models import HomePage, InfoPage


class CmsPagesTest(TestCase):
    def test_homepage_creation(self):
        root = Page.get_first_root_node()
        home = HomePage(title="Inicio")
        root.add_child(instance=home)
        self.assertTrue(home.id)

    def test_info_page_under_home(self):
        root = Page.get_first_root_node()
        home = HomePage(title="Inicio")
        root.add_child(instance=home)
        info = InfoPage(title="Acerca")
        home.add_child(instance=info)
        self.assertTrue(info.id)
