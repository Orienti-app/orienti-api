from django.forms import fields
from django_api_forms import Form


class CreateTokenForm(Form):
    username = fields.EmailField()
    password = fields.CharField()
