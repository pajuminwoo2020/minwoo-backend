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

from board.models import BoardSettlement
from board.serializers import BoardSettlementResponseSerializer, CreateBoardSettlementRequestSerializer, BoardSettlementRequestSerializer, BoardSettlementWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardSettlementView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardSettlement',
        request_body=CreateBoardSettlementRequestSerializer,
        responses={
            200: BoardSettlementResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardSettlement
        """
        serializer = CreateBoardSettlementRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardSettlementResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardSettlementView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardSettlement',
        responses={
            200: BoardSettlementWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardSettlement with the corresponding id
        """
        board = get_object_or_404(BoardSettlement, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardSettlementWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardSettlement',
        request_body=BoardSettlementRequestSerializer,
        responses={
            200: BoardSettlementResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardSettlement with the corresponding id
        """
        board = get_object_or_404(BoardSettlement, pk=board_id)

        serializer = BoardSettlementRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardSettlementResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardSettlement',
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
        Deletes the BoardSettlement with the corresponding id
        """
        board = get_object_or_404(BoardSettlement, pk=board_id)
        if request.user != board.created_by:
            return JsonResponse({'error_message': _('The user does not have permission.')}, status=status.HTTP_400_BAD_REQUEST)

        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardSettlementsView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardSettlements',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardSettlementResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardSettlements at the Institution with the corresponding id
        """
        return self.list(BoardSettlement.objects.all(), BoardSettlementResponseSerializer)
