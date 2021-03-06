import base64
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

from apps.api.errors import ProblemDetailException
from apps.core.models import Token


class BearerBackend(ModelBackend):
    def authenticate(self, request, bearer=None):
        try:
            token = Token.objects.get(pk=bearer, is_active=True)
        except (Token.DoesNotExist, ValidationError):
            raise ProblemDetailException(request, _('Invalid token.'), status=HTTPStatus.UNAUTHORIZED)

        token.user.last_seen_at = timezone.now()
        token.save()

        setattr(request, 'token', token)
        return token.user


class BasicBackend(ModelBackend):
    def authenticate(self, request, basic=None, **kwargs):
        auth_params = base64.b64decode(basic).decode().split(':')
        user = super().authenticate(request, username=auth_params[0], password=auth_params[1])
        if not user:
            raise ProblemDetailException(
                request,
                _('Invalid credentials'),
                status=HTTPStatus.UNAUTHORIZED,
                extra_headers=(
                    ('WWW-Authenticate', f'Bearer realm="{slugify(settings.INSTANCE_NAME)}"'),
                )
            )
        return user


__all__ = [
    'BasicBackend',
    'BearerBackend'
]
