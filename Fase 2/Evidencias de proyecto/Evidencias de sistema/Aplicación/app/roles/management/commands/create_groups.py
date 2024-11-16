from django.core.management.base import BaseCommand
from roles.admin import create_groups

class Command(BaseCommand):
    help = 'Create groups and assign permissions'

    def handle(self, *args, **kwargs):
        create_groups()
        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))
