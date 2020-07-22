import logging

from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser

from board.models import Image
from board.serializers import UploadImageRequestSerializer, ImageResponseSerializer
from board.permissions import  BoardManagementPermission

logger = logging.getLogger('logger')


class ImageView(APIView):
    @swagger_auto_schema(
        tags=['image'],
        operation_id='Get Image',
        responses={
            200: openapi.Schema(type=openapi.TYPE_FILE),
        },
    )
    def get(self, request, image_id, *args, **kwargs):
        """
        Gets image
        """
        image = get_object_or_404(Image, pk=image_id)

        return HttpResponse(image.image_file.read(), content_type='image/png')


class UploadImageView(APIView):
    permission_classes = [IsAuthenticated, BoardManagementPermission]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=['image'],
        operation_id='Create Image',
        request_body=UploadImageRequestSerializer,
        responses={
            200: ImageResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        """
        Uploads a file
        """
        upload_image_serializer = UploadImageRequestSerializer(data=request.data)
        upload_image_serializer.is_valid(raise_exception=True)
        image = upload_image_serializer.save()

        return JsonResponse(ImageResponseSerializer(image, context={'request': request}).data, safe=False, status=status.HTTP_200_OK)
