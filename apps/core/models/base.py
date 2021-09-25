import uuid

from django.db import models

from apps.core.managers.base import BaseManager


class UpdatedAtMixin(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)


class BaseModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BaseManager()

    def update(self, data: dict):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()


__all__ = [
    'UpdatedAtMixin',
    'BaseModel'
]
