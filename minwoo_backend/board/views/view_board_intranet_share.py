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

from board.models import BoardIntranetShare
from board.serializers import BoardIntranetShareResponseSerializer, CreateBoardIntranetShareRequestSerializer, BoardIntranetShareRequestSerializer, BoardIntranetShareWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardIntranetShareView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardIntranetShare',
        request_body=CreateBoardIntranetShareRequestSerializer,
        responses={
            200: BoardIntranetShareResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardIntranetShare
        """
        serializer = CreateBoardIntranetShareRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetShareResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardIntranetShareView(HitCountMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetShare',
        responses={
            200: BoardIntranetShareWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardIntranetShare with the corresponding id
        """
        board = get_object_or_404(BoardIntranetShare, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardIntranetShareWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardIntranetShare',
        request_body=BoardIntranetShareRequestSerializer,
        responses={
            200: BoardIntranetShareResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardIntranetShare with the corresponding id
        """
        board = get_object_or_404(BoardIntranetShare, pk=board_id)

        serializer = BoardIntranetShareRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetShareResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardIntranetShare',
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
        Deletes the BoardIntranetShare with the corresponding id
        """
        board = get_object_or_404(BoardIntranetShare, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardIntranetSharesView(ListModelMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetShares',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardIntranetShareResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardIntranetShares at the Institution with the corresponding id
        """
        return self.list(BoardIntranetShare.objects.all(), BoardIntranetShareResponseSerializer)
