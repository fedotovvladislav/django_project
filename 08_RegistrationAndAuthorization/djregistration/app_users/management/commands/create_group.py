import logging

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


GROUPS = ['moderator', 'verificate', 'standart']
MODELS = ['news model', 'comments model', ]
PERMISSIONS = ['view', ]


class Command(BaseCommand):
    help = 'create users group'

    def handle(self, *args, **kwargs):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = f'Can {permission} {model}'
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                        new_group.permissions.add(model_add_perm)
                    except Permission.DoesNotExist:
                        logging.warning(f"Permission not found with name '{name}'.")
