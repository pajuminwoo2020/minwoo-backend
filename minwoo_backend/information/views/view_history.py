import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView

from information.models import HistoryMain, HistoryAffiliate
from information.serializers import HistoryResponseSerializer
from app.common.utils import SchemaGenerator

logger = logging.getLogger('logger')


def create_histories_list(queryset):
    current_year = queryset.first().date_at.year
    children = []
    histories = [{'year': current_year, 'children': children}]
    for history in queryset:
        if history.date_at.year < current_year:
            current_year = history.date_at.year
            children = [{
                'memo': history.memo,
                'date_at': history.date_at,
            }]
            histories.append({'year': current_year, 'children': children})
        else:
            children.append({
                'memo': history.memo,
                'date_at': history.date_at,
            })

    return histories


class MainHistoriesView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Histories of Minwoo',
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_OBJECT, description='{year: "", children: []'),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of HistoryMain
        """
        main_histories = HistoryMain.objects.all().order_by('-date_at')

        if not main_histories:
            return JsonResponse([], safe=False, status=status.HTTP_200_OK)

        histories = create_histories_list(main_histories)

        return JsonResponse(histories, safe=False, status=status.HTTP_200_OK)


class AffiliateHistoriesView(APIView):
    @swagger_auto_schema(
        tags=['information'],
        operation_id='Get Histories of Affilate',
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_OBJECT, description='{year: "", children: []'),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of HistoryAffiliate
        """
        affiliate_histories = HistoryAffiliate.objects.all().order_by('-date_at')

        if not affiliate_histories:
            return JsonResponse([], safe=False, status=status.HTTP_200_OK)

        histories = create_histories_list(affiliate_histories)

        return JsonResponse(histories, safe=False, status=status.HTTP_200_OK)
