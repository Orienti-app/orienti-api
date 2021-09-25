from datetime import datetime
from typing import Optional
from uuid import UUID

from porcupine.base import Serializer

from apps.api.serializers.users import UserSerializer


class TokenSerializer(Serializer):
    id: UUID
    user: UserSerializer
    expire_at: Optional[datetime] = None
