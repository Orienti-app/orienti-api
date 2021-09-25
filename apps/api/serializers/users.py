from typing import Optional
from uuid import UUID

from porcupine.base import Serializer


class UserSerializer(Serializer):
    id: UUID
    team_id: Optional[UUID] = None
    name: str
    surname: str
    email: str
