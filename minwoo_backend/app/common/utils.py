import base64
import json
import os
import pathlib
import random
import string
from collections import OrderedDict

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from django.utils.datetime_safe import datetime
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from drf_yasg import openapi
from drf_yasg.inspectors import ViewInspector
from drf_yasg.openapi import ReferenceResolver
from drf_yasg.utils import filter_none

from app.common.logger import Logger

class SchemaGenerator:
    @staticmethod
    def _probe_field_inspectors(field, **prop_kwargs):
        inspectors = ViewInspector.field_inspectors
        tried_inspectors = []
        for inspector in inspectors:
            inspector = inspector('', '', '', ReferenceResolver('definitions', force_init=True),
                                  '', field_inspectors=inspectors)
            tried_inspectors.append(inspector)
            method = getattr(inspector, 'field_to_swagger_object', None)
            if method is None:
                continue
            result = method(field, openapi.Schema, True, **prop_kwargs)
            if type(result) is not type(object()):
                break

        return result

    @staticmethod
    def get_field_properties(serializer_class):
        """
        serializer_class의 field들의 schema들을 dictionary 타입으로 만들어 반환
        """
        properties = OrderedDict()

        for property_name, child in serializer_class().fields.items():
            prop_kwargs = {
                'read_only': bool(child.read_only) or None
            }
            prop_kwargs = filter_none(prop_kwargs)

            child_schema = SchemaGenerator._probe_field_inspectors(child, **prop_kwargs)
            properties[property_name] = child_schema

        return properties

    @staticmethod
    def get_required_fields(serializer_class):
        """
        serializer_class의 required field들의 list 반환
        """
        required = []
        for property_name, child in serializer_class().fields.items():
            prop_kwargs = {
                'read_only': bool(child.read_only) or None
            }
            prop_kwargs = filter_none(prop_kwargs)

            child_schema = SchemaGenerator._probe_field_inspectors(child, **prop_kwargs)

            if child.required and not getattr(child_schema, 'read_only', False):
                required.append(property_name)

        return required

    @staticmethod
    def generate_page_schema(serializer_class):
        """
        pagination rule에 맞는 schema 생성
        """
        result = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'contents': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            **SchemaGenerator.get_field_properties(serializer_class),
                        }
                    )
                ),
                'last': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'total': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        )

        return result


def image_directory_path(filename, extension=None):
    """
    file path가 그대로 노출되는것을 막기 위해 random string 등을 조합한 후에 encoding한다.
    """
    random_str = ''.join(random.sample(string.ascii_lowercase, 10))
    extension = extension if extension else get_file_extension(filename)

    return f'image/{str(datetime.today().date())}/{random_str}{urlsafe_base64_encode(force_bytes(filename))}.{extension}'


def get_file_extension(filename):
    if len(filename.split('.')) > 1:
        return filename.split(".")[-1]

    return ''


def file_directory_path(instance, filename):
    """
    file path가 그대로 노출되는것을 막기 위해 random string 등을 조합한 후에 encoding한다.
    """
    random_str = ''.join(random.sample(string.ascii_lowercase, 10))
    extension = get_file_extension(filename)
    if extension:
        return f'file/{str(datetime.today().date())}/{random_str}{urlsafe_base64_encode(force_bytes(filename))}.{extension}'

    return f'file/{str(datetime.today().date())}/{random_str}{urlsafe_base64_encode(force_bytes(filename))}'
