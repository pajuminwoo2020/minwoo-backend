import logging

from django.apps import AppConfig
from django.db.models.signals import post_migrate

logger = logging.getLogger('logger')


def create_default_permissions(sender, **kwargs):
    from django.contrib.auth.models import Group
    from user.models import User

    if Group.objects.filter(name=User.GROUP_STAFF).first() is None:
        Group.objects.create(name=User.GROUP_STAFF)
    if Group.objects.filter(name=User.GROUP_ADMIN).first() is None:
        Group.objects.create(name=User.GROUP_ADMIN)


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        post_migrate.connect(create_default_permissions, sender=self)
