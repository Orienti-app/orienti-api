from http import HTTPStatus

from django.utils.translation import gettext as _

from apps.api.errors import ValidationException, ProblemDetailException
from apps.api.forms.tokens import CreateTokenForm
from apps.api.response import SingleResponse
from apps.api.serializers.tokens import TokenSerializer
from apps.api.views.base import SecuredView
from apps.core.models import Token, User


class TokenManagement(SecuredView):
    UNSECURED_METHODS = ['POST']

    def post(self, request):
        form = CreateTokenForm.create_from_request(request)

        if not form.is_valid():
            raise ValidationException(request, form)

        try:
            user = User.objects.get(email=form.cleaned_data.get('username'))
        except User.DoesNotExist as e:
            raise ProblemDetailException(request, _("Invalid credentials"), status=HTTPStatus.UNAUTHORIZED, previous=e)

        if not user.check_password(form.cleaned_data.get('password')):
            raise ProblemDetailException(request, _("Invalid credentials"), status=HTTPStatus.UNAUTHORIZED)

        token = Token.objects.create(
            user=user
        )

        return SingleResponse(request, token, status=HTTPStatus.OK, serializer=TokenSerializer)
