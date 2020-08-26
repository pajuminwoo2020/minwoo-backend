import logging
import datetime
import pytz

from django.http import JsonResponse
from django.conf import settings
from django.utils.timezone import make_aware
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import Calendar
from information.serializers import CalendarResponseSerializer, CalendarSimpleResponseSerializer, CreateScheduleRequestSerializer, CalendarRequestSerializer
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import OrderingFilter
from board.permissions import  BoardManagementPermission

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


class CreateScheduleView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Create Schedule',
        request_body=CreateScheduleRequestSerializer,
        responses={
            200: CalendarResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a Schedule
        """
        serializer = CreateScheduleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        schedule = serializer.save()

        return JsonResponse(CalendarResponseSerializer(schedule).data, safe=False, status=status.HTTP_200_OK)


class CalendarView(PermissionMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Calendar',
        responses={
            200: CalendarResponseSerializer,
        },
    )
    def get(self, request, calendar_id, *args, **kwargs):
        """
        Gets the Calendar with the corresponding id
        """
        calendar = get_object_or_404(Calendar, pk=calendar_id)

        return JsonResponse(CalendarResponseSerializer(calendar).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Update Calendar',
        request_body=CalendarRequestSerializer,
        responses={
            200: CalendarResponseSerializer,
        },
    )
    def put(self, request, calendar_id, *args, **kwargs):
        """
        Updates the Calendar with the corresponding id
        """
        calendar = get_object_or_404(Calendar, pk=calendar_id)

        serializer = CalendarRequestSerializer(data=request.data, instance=calendar)
        serializer.is_valid(raise_exception=True)
        calendar = serializer.save()

        return JsonResponse(CalendarResponseSerializer(calendar).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['information'],
        operation_id='Delete Calendar',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        },
    )
    def delete(self, request, calendar_id, *args, **kwargs):
        """
        Deletes the Calendar with the corresponding id
        """
        calendar = get_object_or_404(Calendar, pk=calendar_id)
        calendar.delete()

        return JsonResponse({'id': calendar_id}, safe=False, status=status.HTTP_200_OK)
