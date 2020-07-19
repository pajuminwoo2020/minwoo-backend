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

from board.models import BoardActivityMember
from board.serializers import BoardActivityMemberResponseSerializer, CreateBoardActivityMemberRequestSerializer, BoardActivityMemberRequestSerializer, BoardActivityMemberWithBodyResponseSerializer
from app.common.mixins import PermissionMixin, ListModelMixin
from app.common.utils import SchemaGenerator
from app.common.filters import SearchFilter, OrderingFilter

logger = logging.getLogger('logger')


class CreateBoardActivityMemberView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Create BoardActivityMember',
        request_body=CreateBoardActivityMemberRequestSerializer,
        responses={
            200: BoardActivityMemberResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Creates an BoardActivityMember
        """
        serializer = CreateBoardActivityMemberRequestSerializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardActivityMemberResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)


class BoardActivityMemberView(PermissionMixin, HitCountMixin, APIView):
    permission_classes = {
        'get': [],
        'put': [IsAuthenticated],
        'delete': [IsAuthenticated],
    }

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardActivityMember',
        responses={
            200: BoardActivityMemberWithBodyResponseSerializer,
        },
    )
    def get(self, request, board_id, *args, **kwargs):
        """
        Gets the BoardActivityMember with the corresponding id
        """
        board = get_object_or_404(BoardActivityMember, pk=board_id)
        self.hit_count(request, board.hit_count)

        return JsonResponse(BoardActivityMemberWithBodyResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Update BoardActivityMember',
        request_body=BoardActivityMemberRequestSerializer,
        responses={
            200: BoardActivityMemberResponseSerializer,
        },
    )
    def put(self, request, board_id, *args, **kwargs):
        """
        Updates the BoardActivityMember with the corresponding id
        """
        board = get_object_or_404(BoardActivityMember, pk=board_id)

        serializer = BoardActivityMemberRequestSerializer(data=request.data, instance=board, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        return JsonResponse(BoardActivityMemberResponseSerializer(board).data, safe=False, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Delete BoardActivityMember',
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
        Deletes the BoardActivityMember with the corresponding id
        """
        board = get_object_or_404(BoardActivityMember, pk=board_id)
        if request.user != board.created_by:
            return JsonResponse({'error_message': _('The user does not have permission.')}, status=status.HTTP_400_BAD_REQUEST)

        board.delete()

        return JsonResponse({'id': board_id}, safe=False, status=status.HTTP_200_OK)


class BoardActivityMembersView(ListModelMixin, APIView):
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['created_by__fullname', 'title']
    ordering_default = ['-created_at']

    @swagger_auto_schema(
        tags=['board'],
        operation_id='Get BoardActivityMembers',
        responses={
            200: SchemaGenerator.generate_page_schema(BoardActivityMemberResponseSerializer),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets a list of BoardActivityMembers at the Institution with the corresponding id
        """
        return self.list(BoardActivityMember.objects.all(), BoardActivityMemberResponseSerializer)
