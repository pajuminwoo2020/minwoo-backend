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

from board.models import BoardPress
from board.serializers import BoardPressResponseSerializer, CreateBoardPressRequestSerializer, BoardPressRequestSerializer, BoardPressWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardPressView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardPress',
        request_body=CreateBoardPressRequestSerializer,
        responses={
            200: BoardPressResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardPress
        """
        serializer = CreateBoardPressRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardPressResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardPressView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardPress',
        responses={
            200: BoardPressWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardPress with the corresponding id
        """
        board = get_object_or_404(BoardPress, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardPressWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardPress',
        request_body=BoardPressRequestSerializer,
        responses={
            200: BoardPressResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardPress with the corresponding id
        """
        board = get_object_or_404(BoardPress, pk=board_id)

        serializer = BoardPressRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardPressResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardPress',
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
        Deletes the BoardPress with the corresponding id
        """
        board = get_object_or_404(BoardPress, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardPressesView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardPresses',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardPressResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardPresses at the Institution with the corresponding id
        """
        return self.list(BoardPress.objects.all(), BoardPressResponseSerializer)
