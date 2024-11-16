from django.db.models.signals import post_migrate
from django.dispatch import receiver
from roles.admin import create_groups


@receiver(post_migrate)
def create_groups_after_migration(sender, **kwargs):
    create_groups()
