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

from board.models import BoardNotice
from board.serializers import BoardNoticeResponseSerializer, CreateBoardNoticeRequestSerializer, BoardNoticeRequestSerializer, BoardNoticeWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter, CategoryFilter

logger = logging.getLogger('logger')


class CreateBoardNoticeView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardNotice',
        request_body=CreateBoardNoticeRequestSerializer,
        responses={
            200: BoardNoticeResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardNotice
        """
        serializer = CreateBoardNoticeRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardNoticeResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardNoticeView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardNotice',
        responses={
            200: BoardNoticeWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardNotice with the corresponding id
        """
        board = get_object_or_404(BoardNotice, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardNoticeWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardNotice',
        request_body=BoardNoticeRequestSerializer,
        responses={
            200: BoardNoticeResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardNotice with the corresponding id
        """
        board = get_object_or_404(BoardNotice, pk=board_id)

        serializer = BoardNoticeRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardNoticeResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardNotice',
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
        Deletes the BoardNotice with the corresponding id
        """
        board = get_object_or_404(BoardNotice, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardNoticesView(ListModelMixin, APIView):
    filter_backends = [CategoryFilter, SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardNotices',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardNoticeResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardNotices
        """
        return self.list(BoardNotice.objects.all(), BoardNoticeResponseSerializer)
