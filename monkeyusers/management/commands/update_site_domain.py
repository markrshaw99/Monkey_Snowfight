from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Update Django site domain to fix email headers'

    def handle(self, *args, **options):
        try:
            site = Site.objects.get(pk=1)
            site.domain = 'monkey-snowfight-game-and-chat-ce8d3c703935.herokuapp.com'
            site.name = 'Monkey Snowfight'
            site.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Successfully updated site domain to: {site.domain}'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Site name set to: {site.name}'
                )
            )
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('❌ Site with ID 1 does not exist')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error updating site: {e}')
            )
