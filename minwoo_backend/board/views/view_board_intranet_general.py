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

from board.models import BoardIntranetGeneral
from board.serializers import BoardIntranetGeneralResponseSerializer, CreateBoardIntranetGeneralRequestSerializer, BoardIntranetGeneralRequestSerializer, BoardIntranetGeneralWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardIntranetGeneralView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardIntranetGeneral',
        request_body=CreateBoardIntranetGeneralRequestSerializer,
        responses={
            200: BoardIntranetGeneralResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardIntranetGeneral
        """
        serializer = CreateBoardIntranetGeneralRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetGeneralResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardIntranetGeneralView(HitCountMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetGeneral',
        responses={
            200: BoardIntranetGeneralWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardIntranetGeneral with the corresponding id
        """
        board = get_object_or_404(BoardIntranetGeneral, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardIntranetGeneralWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardIntranetGeneral',
        request_body=BoardIntranetGeneralRequestSerializer,
        responses={
            200: BoardIntranetGeneralResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardIntranetGeneral with the corresponding id
        """
        board = get_object_or_404(BoardIntranetGeneral, pk=board_id)

        serializer = BoardIntranetGeneralRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardIntranetGeneralResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardIntranetGeneral',
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
        Deletes the BoardIntranetGeneral with the corresponding id
        """
        board = get_object_or_404(BoardIntranetGeneral, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardIntranetGeneralsView(ListModelMixin, APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardIntranetGenerals',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardIntranetGeneralResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardIntranetGenerals at the Institution with the corresponding id
        """
        return self.list(BoardIntranetGeneral.objects.all(), BoardIntranetGeneralResponseSerializer)
