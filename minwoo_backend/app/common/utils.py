import base64
import json
import os
import pathlib

import boto3
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMultiAlternatives
from sendgrid import Mail, TrackingSettings, ClickTracking, OpenTracking, Email, SendGridAPIClient, Attachment, FileContent, FileName, Disposition, FileType
#from loggedemail.models import LoggedEmailManager


from collections import OrderedDict

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
