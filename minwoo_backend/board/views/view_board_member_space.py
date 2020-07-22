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

from board.models import BoardMemberSpace
from board.serializers import BoardMemberSpaceResponseSerializer, CreateBoardMemberSpaceRequestSerializer, BoardMemberSpaceRequestSerializer, BoardMemberSpaceWithBodyResponseSerializer
from board.permissions import  BoardManagementPermission
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardMemberSpaceView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardMemberSpace',
        request_body=CreateBoardMemberSpaceRequestSerializer,
        responses={
            200: BoardMemberSpaceResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardMemberSpace
        """
        serializer = CreateBoardMemberSpaceRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardMemberSpaceResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardMemberSpaceView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated, BoardManagementPermission],
        'delete': [IsAuthenticated, BoardManagementPermission],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardMemberSpace',
        responses={
            200: BoardMemberSpaceWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardMemberSpace with the corresponding id
        """
        board = get_object_or_404(BoardMemberSpace, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardMemberSpaceWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardMemberSpace',
        request_body=BoardMemberSpaceRequestSerializer,
        responses={
            200: BoardMemberSpaceResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardMemberSpace with the corresponding id
        """
        board = get_object_or_404(BoardMemberSpace, pk=board_id)

        serializer = BoardMemberSpaceRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardMemberSpaceResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardMemberSpace',
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
        Deletes the BoardMemberSpace with the corresponding id
        """
        board = get_object_or_404(BoardMemberSpace, pk=board_id)
        if request.user != board.created_by:
            return JsonResponse({'error_message': _('The user does not have permission.')}, status=status.HTTP_400_BAD_REQUEST)

        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardMemberSpacesView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardMemberSpaces',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardMemberSpaceResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardMemberSpaces at the Institution with the corresponding id
        """
        return self.list(BoardMemberSpace.objects.all(), BoardMemberSpaceResponseSerializer)
