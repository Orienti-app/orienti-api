import json
from dataclasses import dataclass
from http import HTTPStatus
from typing import Type, Union, List

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.translation import gettext as _
from porcupine.base import Serializer

from apps.api.encoders import ApiJSONEncoder
from apps.api.errors import ValidationException, ProblemDetailException
from apps.core.models.base import BaseModel


@dataclass
class Ordering:
    columns: List[str]

    @classmethod
    def create_from_request(cls, request, aliases: dict = None) -> 'Ordering':
        columns = []
        aliases = aliases or {}

        for column in request.GET.get('order_by', 'created_at').split(','):
            column_name = column[1:] if column.startswith("-") else column
            if column_name in aliases.keys():
                columns.append(
                    f"-{aliases[column_name]}" if column.startswith("-") else aliases[column_name]
                )
            else:
                columns.append(column)

        result = Ordering(columns)
        return result

    def __str__(self):
        return ",".join(self.columns)

    def __repr__(self):
        return self.__str__()


class GeneralResponse(HttpResponse):
    def __init__(self, request, data: Union[BaseModel, dict] = None, serializer: Type[Serializer] = None, **kwargs):
        params = {}
        if data is not None:
            content_type = request.headers.get('accept', 'application/json')
            if content_type in ['*/*', 'application/json']:
                params['content_type'] = 'application/json'
                params['content'] = json.dumps(data, cls=ApiJSONEncoder, serializer=serializer)
            else:
                params['content_type'] = 'application/json'
                params['status'] = HTTPStatus.NOT_ACCEPTABLE
                params['content'] = json.dumps({
                    'message': _("Not Acceptable"),
                    'metadata': {
                        'available': [
                            'application/json',
                        ],
                        'asked': content_type
                    }
                })

        kwargs.update(params)
        super().__init__(**kwargs)


class SingleResponse(GeneralResponse):
    def __init__(self, request, data=None, **kwargs):
        if data is None:
            kwargs['status'] = HTTPStatus.NO_CONTENT
        else:
            data = {
                'response': data,
            }
        super().__init__(request=request, data=data, **kwargs)


class ErrorResponse(GeneralResponse):
    def __init__(self, request, payload: dict, **kwargs):
        super().__init__(request=request, data=payload, **kwargs)

    @staticmethod
    def create_from_exception(e: ProblemDetailException) -> 'ErrorResponse':
        return ErrorResponse(e.request, e.payload, status=e.status, headers=e.extra_headers)


class ValidationResponse(GeneralResponse):
    def __init__(self, request, payload: dict, **kwargs):
        data = {
            'type': '/validation-error',
            'title': 'Invalid request parameters',
            'status': HTTPStatus.UNPROCESSABLE_ENTITY,
            'errors': payload,
        }

        super().__init__(request, data, status=HTTPStatus.UNPROCESSABLE_ENTITY, **kwargs)

    @staticmethod
    def create_from_exception(e: ValidationException) -> 'ValidationResponse':
        return ValidationResponse(e.request, e.payload, status=HTTPStatus.UNPROCESSABLE_ENTITY)


class PaginationResponse(GeneralResponse):
    def __init__(
        self, request, qs, page: Union[int, None] = None, limit: Union[int, None] = None, ordering: Ordering = None,
        **kwargs
    ):
        kwargs.setdefault('content_type', 'application/json')

        # Ordering
        ordering = ordering if ordering else Ordering.create_from_request(request)
        qs = qs.order_by(str(ordering))

        if limit is None:
            data = {
                'items': qs,
                'metadata': {
                    'page': int(request.GET.get('page', 1)) if not page else page,
                    'limit': None,
                    'pages': 1,
                    'total': qs.count()
                }
            }
        else:
            paginator = Paginator(qs, limit)

            data = {
                'items': paginator.get_page(page),
                'metadata': {
                    'page': int(page),
                    'limit': paginator.per_page,
                    'pages': paginator.num_pages,
                    'total': paginator.count
                }
            }

        super().__init__(request, data, **kwargs)


__all__ = [
    'SingleResponse',
    'ErrorResponse',
    'PaginationResponse',
    'ValidationResponse',
    'Ordering'
]
