import logging
import datetime
import pytz

from django.http import JsonResponse
from django.conf import settings
from django.utils.timezone import make_aware
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import Calendar
from information.serializers import CalendarResponseSerializer, CalendarSimpleResponseSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import OrderingFilter

logger = logging.getLogger('logger')


class CalendarsAllView(ListModelMixin, APIView):
    filter_backends = [OrderingFilter]
    ordering_default = ['schedule_from']

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Calendars',
        manual_parameters=[
            openapi.Parameter('selected_date', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING),
        ],
        responses={
            200: SchemaGenerator.generate_page_schema(CalendarSimpleResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of Calendars
        """
        selected_date = request.GET.get('selected_date')
        if selected_date:
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
        else:
            selected_date = datetime.datetime.now()

        schedules = Calendar.objects.filter(
            Q(schedule_from__gte=selected_date - datetime.timedelta(days=42)) &
            Q(schedule_from__lte=selected_date + datetime.timedelta(days=42))
        )

        return self.list(schedules, CalendarSimpleResponseSerializer)


class CalendarsView(ListModelMixin, APIView):
    filter_backends = [OrderingFilter]
    ordering_default = ['schedule_from']

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Calendar',
        manual_parameters=[
            openapi.Parameter('selected_date', openapi.IN_QUERY, description='YYYY-MM-DD', type=openapi.TYPE_STRING),
        ],
        responses={
            200: SchemaGenerator.generate_page_schema(CalendarResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets the schedules at the selected date
        """
        selected_date = request.GET.get('selected_date')
        if selected_date:
            selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d')
        else:
            selected_date = datetime.datetime.now()

        selected_date_start = make_aware(
            selected_date.replace(hour=0, minute=0, second=0),
            timezone=pytz.timezone(settings.TIME_ZONE_ASIA_SEOUL)
        )
        selected_date_end = make_aware(
            selected_date.replace(hour=23, minute=59, second=59),
            timezone=pytz.timezone(settings.TIME_ZONE_ASIA_SEOUL)
        )

        schedules = Calendar.objects.filter(
            Q(schedule_from__gte=selected_date_start) &
            Q(schedule_from__lte=selected_date_end)
        )

        return self.list(schedules, CalendarResponseSerializer)
