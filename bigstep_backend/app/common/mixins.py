import logging
from collections import OrderedDict

from django.core.paginator import InvalidPage
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.mixins import ListModelMixin as BaseListModelMixin
from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.settings import api_settings

logger = logging.getLogger('quotalogger')


class PageNumberPagination(BasePageNumberPagination):
    start_offset = 1
    page_size_query_param = 'pageSize'
    page_query_param = 'current'
    page_query_description = 'A page number({0}-based) ' \
                             'within the paginated result set. Default: {0}'.format(start_offset)
    page_size_query_description = f'Number of results to return per page. Default: {api_settings.PAGE_SIZE}'

    def get_offset(self):
        return self.start_offset - 1

    def get_paginated_response(self, data):
        return JsonResponse(OrderedDict([
            ('contents', data),
            ('last', self.page.number == self.page.paginator.num_pages),
            ('total', self.page.paginator.count),
        ]), safe=False, status=status.HTTP_200_OK)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        # page_number: 1-based offset 
        page_number = request.query_params.get(self.page_query_param, self.start_offset)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages + self.get_offset()

        page_number = str(int(page_number) - self.get_offset())

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=str(int(page_number) + self.get_offset()), message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request

        return list(self.page)


class ListModelMixin(BaseListModelMixin):
    """
    List a queryset.
    """
    pagination_class = PageNumberPagination
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS

    def list(self, queryset, serializer_class, **kwargs):
        queryset = self._filter_queryset(queryset)
        queryset = self._filter_serializer(queryset, serializer_class, **kwargs)

        page = self._paginate_queryset(queryset)
        if page is not None:
            return self._get_paginated_response((serializer_class(page, many=True, **kwargs).data))

        return JsonResponse(serializer_class(queryset, many=True, **kwargs).data, safe=False, status=status.HTTP_200_OK)

    def _filter_queryset(self, queryset):
        if isinstance(queryset, list):
            logger.info('Type of queryset is not QuerySet, but list. Skip filtering')

            return queryset

        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    def _filter_serializer(self, queryset, serializer_class, **kwargs):
        search_word = self.request.query_params.get('q', '')
        if not hasattr(self, 'serializer_fields_filter') or not isinstance(self.serializer_fields_filter, list) or search_word == '':
            return queryset
        serializer_results = serializer_class(queryset, many=True, **kwargs).data
        target_id = []
        for serializer_result in serializer_results:
            for filters in self.serializer_fields_filter:
                keys = filters.split('__')
                target_dict = serializer_result
                for key in keys[:-1]:
                    target_dict = target_dict.get(key, {})
                if search_word.lower() in target_dict.get(keys[-1:][0], '').lower() and serializer_result.get('id', '') not in target_id:
                    target_id.append(serializer_result.get('id', ''))
        return queryset.filter(id__in=target_id)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def _paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def _get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class TreeModelMixin:
    """
    Get Json Tree of node
    """

    def tree(self, node):
        json_tree = self._recursive_node_to_dict(node)

        return JsonResponse(json_tree, safe=False, status=status.HTTP_200_OK)

    def _recursive_node_to_dict(self, node):
        result = {
            'title': node.name,
            'key': '-'.join([str(node.pk) for node in node.get_ancestors(include_self=True)]),
        }
        children = [self._recursive_node_to_dict(c) for c in node.get_children()]
        if children:
            result['children'] = children

        return result


class PermissionMixin:
    def get_permissions(self):
        try:
            # return permission_classes depending on http method
            return [permission() for permission in self.permission_classes[self.request.method.lower()]]
        except KeyError:
            return [IsAuthenticated()]
