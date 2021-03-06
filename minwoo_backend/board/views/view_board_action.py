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

from board.models import BoardAction, BoardAffiliateActivity, Category
from board.serializers import BoardActionResponseSerializer, CreateBoardActionRequestSerializer, BoardActionRequestSerializer, BoardActionWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter, CategoryFilter

logger = logging.getLogger('logger')


class CreateBoardActionView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardAction',
        request_body=CreateBoardActionRequestSerializer,
        responses={
            200: BoardActionResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardAction
        """
        serializer = CreateBoardActionRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardActionResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardActionView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardAction',
        responses={
            200: BoardActionWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardAction with the corresponding id
        """
        board = get_object_or_404(BoardAction, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardActionWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardAction',
        request_body=BoardActionRequestSerializer,
        responses={
            200: BoardActionResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardAction with the corresponding id
        """
        board = get_object_or_404(BoardAction, pk=board_id)

        serializer = BoardActionRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardActionResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardAction',
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
        Deletes the BoardAction with the corresponding id
        """
        board = get_object_or_404(BoardAction, pk=board_id)
        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardActionsView(ListModelMixin, APIView):
    filter_backends = [CategoryFilter, SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardActions',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardActionResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardActions at the Institution with the corresponding id
        """
        queryset = []
        queryset += self._filter_queryset(BoardAction.objects.all())
        queryset += self._filter_queryset(BoardAffiliateActivity.objects.filter(on_board_action=Category.TYPE_BOARD_ACTION).all())

        queryset = sorted(queryset, key=lambda obj: obj.created_at, reverse=True)
        page = self._paginate_queryset(queryset)
        if page is not None:
            return self._get_paginated_response((BoardActionResponseSerializer(page, many=True, **kwargs).data))

        return JsonResponse(BoardActionResponseSerializer(queryset, many=True, **kwargs).data, safe=False, status=status.HTTP_200_OK)
