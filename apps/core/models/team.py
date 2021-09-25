from django.db import models

from apps.core.models.base import UpdatedAtMixin, BaseModel


class Team(BaseModel, UpdatedAtMixin):
    class Meta:
        app_label = 'core'
        db_table = 'teams'
        default_permissions = ()

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)


__all__ = [
    'Team'
]
