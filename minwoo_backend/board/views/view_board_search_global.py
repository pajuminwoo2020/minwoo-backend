import logging

from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.views import APIView
from board.models import BoardBase, BoardIntranetDrive, BoardIntranetShare
from board.serializers import BoardCommonResponseSerializer
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')

class BoardSearchGlobalView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get Board Posts',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardCommonResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of posts
        """
        from django.apps import apps
        def get_subclasses(abstract_class):
           result = []
           for model in apps.get_app_config('board').get_models():
              if issubclass(model, abstract_class) and model is not abstract_class and model is not BoardIntranetDrive and model is not BoardIntranetShare:
                   result.append(model)
           return result

        queryset = []
        for board in get_subclasses(BoardBase):
            boards = board.objects.all()
            queryset += self._filter_queryset(boards)

        queryset = sorted(queryset, key=lambda obj: obj.created_at, reverse=True)
        page = self._paginate_queryset(queryset)
        if page is not None:
            return self._get_paginated_response((BoardCommonResponseSerializer(page, many=True, **kwargs).data))

        return JsonResponse(BoardCommonResponseSerializer(queryset, many=True, **kwargs).data, safe=False, status=status.HTTP_200_OK)
