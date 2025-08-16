from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from cms.models import HomePage


class Command(BaseCommand):
    help = 'Setup initial Wagtail site configuration'

    def handle(self, *args, **options):
        # Get the default Site
        try:
            site = Site.objects.get(is_default_site=True)
            self.stdout.write(f"Found default site: {site}")
        except Site.DoesNotExist:
            self.stdout.write("No default site found, creating one...")
            site = Site.objects.create(
                hostname='localhost',
                port=8000,
                site_name='deferia.cr',
                is_default_site=True
            )

        # Check if we already have a HomePage
        try:
            home_page = HomePage.objects.get()
            self.stdout.write(f"HomePage already exists: {home_page}")
        except HomePage.DoesNotExist:
            # Create a new HomePage
            root_page = Page.objects.get(id=1)  # This is the Wagtail root page
            
            home_page = HomePage(
                title="Inicio",
                slug="inicio",
                hero_title="Bienvenido a deferia.cr"
            )
            
            root_page.add_child(instance=home_page)
            
            # Set this as the site's root page
            site.root_page = home_page
            site.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created HomePage: {home_page}')
            )
            
        except HomePage.MultipleObjectsReturned:
            home_page = HomePage.objects.first()
            self.stdout.write(f"Multiple HomePage objects found, using: {home_page}")

        self.stdout.write(
            self.style.SUCCESS('Wagtail site setup completed successfully!')
        )
