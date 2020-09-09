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

from board.models import BoardDrive
from board.serializers import BoardDriveResponseSerializer, CreateBoardDriveRequestSerializer, BoardDriveRequestSerializer, BoardDriveWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardDriveView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardDrive',
        request_body=CreateBoardDriveRequestSerializer,
        responses={
            200: BoardDriveResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardDrive
        """
        serializer = CreateBoardDriveRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardDriveResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardDriveView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardDrive',
        responses={
            200: BoardDriveWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardDrive with the corresponding id
        """
        board = get_object_or_404(BoardDrive, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardDriveWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardDrive',
        request_body=BoardDriveRequestSerializer,
        responses={
            200: BoardDriveResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardDrive with the corresponding id
        """
        board = get_object_or_404(BoardDrive, pk=board_id)

        serializer = BoardDriveRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardDriveResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardDrive',
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
        Deletes the BoardDrive with the corresponding id
        """
        board = get_object_or_404(BoardDrive, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardDrivesView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardDrives',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardDriveResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardDrives at the Institution with the corresponding id
        """
        return self.list(BoardDrive.objects.all(), BoardDriveResponseSerializer)
