import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from hitcount.views import HitCountMixin

from board.models import BoardAffiliateActivity
from board.serializers import BoardAffiliateActivityResponseSerializer, CreateBoardAffiliateActivityRequestSerializer, BoardAffiliateActivityRequestSerializer, BoardAffiliateActivityWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardAffiliateActivityView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardAffiliateActivity',
        request_body=CreateBoardAffiliateActivityRequestSerializer,
        responses={
            200: BoardAffiliateActivityResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardAffiliateActivity
        """
        serializer = CreateBoardAffiliateActivityRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardAffiliateActivityResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardAffiliateActivityView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardAffiliateActivity',
        responses={
            200: BoardAffiliateActivityWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardAffiliateActivity with the corresponding id
        """
        board = get_object_or_404(BoardAffiliateActivity, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardAffiliateActivityWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardAffiliateActivity',
        request_body=BoardAffiliateActivityRequestSerializer,
        responses={
            200: BoardAffiliateActivityResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardAffiliateActivity with the corresponding id
        """
        board = get_object_or_404(BoardAffiliateActivity, pk=board_id)

        serializer = BoardAffiliateActivityRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardAffiliateActivityResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardAffiliateActivity',
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                },
            ),
        },
    )
    def delete(self, request, board_id, *args, **kwargs):
        """
        Deletes the BoardAffiliateActivity with the corresponding id
        """
        board = get_object_or_404(BoardAffiliateActivity, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardAffiliateActivitiesView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardAffiliateActivities',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardAffiliateActivityResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardAffiliateActivities
        """
        return self.list(BoardAffiliateActivity.objects.all(), BoardAffiliateActivityResponseSerializer)
