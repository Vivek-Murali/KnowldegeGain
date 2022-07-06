import logging
import typing

import django.db
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpRequest, HttpResponse
from rest_framework.parsers import JSONParser
from django.core.serializers.json import DjangoJSONEncoder
import json
from .serializers import UserActivitySerializer
from django.utils import timezone

from django.conf import settings
from .models import UserVisit

from .settings import RECORDING_BYPASS, RECORDING_DISABLED

logger = logging.getLogger(__name__)


def save_user_visit(user_visit: UserVisit) -> None:
    """Save the user visit and handle db.IntegrityError."""
    try:
        """ _data = json.loads(json.dumps(user_visit,cls=DjangoJSONEncoder))
        _serializer = UserActivitySerializer(data=_data)
        if _serializer.is_valid():
            _serializer.save() """ 
        settings.DATABASE['user_user_visit'].insert(user_visit)
    except Exception as e:
        logger.warning("Error saving user visit (hash='%s')", user_visit.hash)


class UserVisitMiddleware:
    """Middleware to record user visits."""

    def __init__(self, get_response: typing.Callable) -> None:
        if RECORDING_DISABLED:
            raise MiddlewareNotUsed("UserVisit recording has been disabled")
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> typing.Optional[HttpResponse]:
        if request.user.is_anonymous:
            return self.get_response(request)

        if RECORDING_BYPASS(request):
            return self.get_response(request)

        uv,uv_hash = UserVisit.objects.build(request, timezone.now())
        if not UserVisit.objects.filter(hash=uv_hash).exists():
            save_user_visit(uv)

        return self.get_response(request)
