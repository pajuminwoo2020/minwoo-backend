import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView

from board.models import Category

logger = logging.getLogger('logger')


class SelectCategoriesView(APIView):
    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get Selectable Categories at board',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.TYPE_OBJECT,
                description='{value: "", label: ""}',
            ),
        },
    )
    def get(self, request, board_type, *args, **kwargs):
        """
        Gets Categories list at the corresponding board type.
        """
        result = []
        for category in Category.objects.filter(board_type=board_type).all():
            result.append({
                'value': category.pk,
                'label': category.name,
            })

        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
