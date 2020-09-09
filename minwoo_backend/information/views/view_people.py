import logging

from django.http import JsonResponse
from django.db.models import F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from information.models import People, PeopleImage
from information.serializers import PeopleResponseSerializer
from app.common.mixins import ListModelMixin

logger = logging.getLogger('logger')


def create_people_list(queryset):
    """
    조직도 리스트 리턴하는 함수. 추후 요청에 의해 삭제됐으나 일단 코드는 남겨둠
    """
    result = []
    for person in queryset:
        person_in_position = list(filter(lambda x : x.get('position') == person.position, result))
        if person_in_position:
            children = person_in_position[0].get('children', [])
            children.append({
                'name': person.name,
                'job': person.job,
            })
        else:
            children = [{
                'name': person.name,
                'job': person.job,
            }]
            result.append({'position': person.position, 'children': children})

    return result


class PeopleView(APIView):
    @swagger_auto_schema(
        tags=['people'],
        operation_id='Get People',
        responses={
            200: openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_OBJECT, description='{position: "", children: []'),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Gets people
        """
        people_image = PeopleImage.objects.order_by('created_at').last()

        return JsonResponse({'absolute_url': people_image.get_image_absolute_url()}, safe=False, status=status.HTTP_200_OK)
