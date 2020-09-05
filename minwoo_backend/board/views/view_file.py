import logging
import mimetypes
import re
from urllib.parse import quote

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser

from board.models import File, BoardIntranetDrive, BoardIntranetShare, BoardIntranetGeneral
from board.serializers import UploadFileRequestSerializer, FileResponseSerializer
from board.permissions import  BoardManagementPermission

logger = logging.getLogger('logger')


def _create_file_response(file_instance):
    if file_instance.file:
        (mimetype, encoding) = mimetypes.guess_type(file_instance.file.name)
        file = file_instance.file

        file_name_quoted = quote(file_instance.file_name.encode('utf-8'), safe='')
        response = HttpResponse(file, content_type=mimetype)
        response['Content-Disposition'] = f'attachment; filename="{file_name_quoted}"; filename*=UTF-8\'\'{file_name_quoted}'
        logger.info(f'Returning file response for File={file}')

        return response

    # send error if nothing was provided
    logger.warning(f'Non existing file or url for File={file}')

    return HttpResponseNotFound()


class UploadFileView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['file'],
        operation_id='Create File',
        request_body=UploadFileRequestSerializer,
        responses={
            200: FileResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Uploads a file
        """
        upload_file_serializer = UploadFileRequestSerializer(data=request.data)
        upload_file_serializer.is_valid(raise_exception=True)
        file = upload_file_serializer.save()

        return JsonResponse(FileResponseSerializer(file, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)


class FileView(APIView):
    @swagger_auto_schema(
        tags=['file'],
        operation_id='Get File',
        responses={
            200: openapi.Schema(type=openapi.TYPE_FILE),
        },
    )
    def get(self, request, uidb64, *args, **kwargs):
        """
        Gets the file
        """
        uidb64_number = re.findall('\d+', force_text(urlsafe_base64_decode(uidb64)))
        file_id = uidb64_number[0] if uidb64_number else '0'
        file_instance = get_object_or_404(File, pk=file_id)
        # 인트라넷 게시판 파일 접근 권한체크
        if isinstance(file_instance.board_at, BoardIntranetDrive) or isinstance(file_instance.board_at, BoardIntranetShare):
            if not BoardManagementPermission().has_permission(request, self):
                return HttpResponseForbidden()

        return _create_file_response(file_instance)
