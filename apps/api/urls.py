from django.urls import path

from apps.api.views import tokens

urlpatterns = [
    path('tokens', tokens.TokenManagement.as_view(), name='token-management'),
]
