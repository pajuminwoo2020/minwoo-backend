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

from board.models import BoardIntranetDrive
from board.serializers import BoardIntranetDriveResponseSerializer, CreateBoardIntranetDriveRequestSerializer, BoardIntranetDriveRequestSerializer, BoardIntranetDriveWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardIntranetDriveView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardIntranetDrive',
        request_body=CreateBoardIntranetDriveRequestSerializer,
        responses={
            200: BoardIntranetDriveResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardIntranetDrive
        """
        serializer = CreateBoardIntranetDriveRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetDriveResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardIntranetDriveView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetDrive',
        responses={
            200: BoardIntranetDriveWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardIntranetDrive with the corresponding id
        """
        board = get_object_or_404(BoardIntranetDrive, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardIntranetDriveWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardIntranetDrive',
        request_body=BoardIntranetDriveRequestSerializer,
        responses={
            200: BoardIntranetDriveResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardIntranetDrive with the corresponding id
        """
        board = get_object_or_404(BoardIntranetDrive, pk=board_id)

        serializer = BoardIntranetDriveRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetDriveResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardIntranetDrive',
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
        Deletes the BoardIntranetDrive with the corresponding id
        """
        board = get_object_or_404(BoardIntranetDrive, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardIntranetDrivesView(ListModelMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetDrives',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardIntranetDriveResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardIntranetDrives at the Institution with the corresponding id
        """
        return self.list(BoardIntranetDrive.objects.all(), BoardIntranetDriveResponseSerializer)
