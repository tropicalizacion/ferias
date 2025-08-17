from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from wagtail.models import Page, Site

from apps.cms_pages.models import HomePage


class Command(BaseCommand):
    help = "Initialize Wagtail with a default site and homepage if missing."

    def handle(self, *args, **options):
        # Create root homepage if not exists
        root = Page.get_first_root_node()
        if not HomePage.objects.live().exists():
            home = HomePage(title="Inicio")
            root.add_child(instance=home)
            home.save_revision().publish()
            self.stdout.write(self.style.SUCCESS("Created HomePage and published it."))
        else:
            home = HomePage.objects.live().first()
            self.stdout.write("HomePage already exists: %s" % home)

        # Ensure default Site points to our homepage
        site, created = Site.objects.get_or_create(
            hostname="localhost",
            defaults={
                "root_page": home,
                "site_name": "deferia.cr",
                "is_default_site": True,
            },
        )
        if not created:
            if site.root_page_id != home.id:
                site.root_page = home
                site.is_default_site = True
                site.save()
                self.stdout.write(self.style.SUCCESS("Updated default Site root_page."))
        else:
            self.stdout.write(self.style.SUCCESS("Created default Site entry."))

        self.stdout.write(self.style.SUCCESS("Wagtail initialization complete."))
