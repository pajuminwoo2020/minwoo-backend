import operator
from functools import reduce

from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.db.models.sql.constants import ORDER_PATTERN
from django.utils.encoding import force_str
from rest_framework.compat import coreapi, coreschema
from rest_framework.compat import distinct
from rest_framework.filters import SearchFilter as BaseSearchFilter, OrderingFilter as BaseOrderingFilter, BaseFilterBackend


class SearchFilter(BaseSearchFilter):
    search_param = 'q'
    lookup_prefixes = {
        '^': 'istartswith',
        '=': 'iexact',
        '@': 'search',
        '$': 'iregex',
        '#': 'external_func',  # model instance의 python method를 호출하는 경우 사용
    }

    def _construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if not lookup:
            lookup = 'icontains'
        elif lookup == 'external_func':
            return None
        else:
            field_name = field_name[1:]

        return LOOKUP_SEP.join([field_name, lookup])

    def _filter_by_external_func(self, queryset_by_func_ids, func, queryset, search_terms):
        """
        각각의 row(model instance)마다 func의 return value를 구한 다음, search_term을 포함하면 queryset_by_func_ids에 추가.
        eval 사용은 조심해야하지만 func는 내부에서만 생성되는 값이기 때문에 문제없어보임.
        """
        for instance in queryset:
            field_value = eval(f'instance.{func}')
            [queryset_by_func_ids.append(instance.pk) for search_term in search_terms if search_term.lower() in field_value.lower()]

    def filter_queryset(self, request, queryset, view):
        """
        Case-insensitive search filtering
        """
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = []
        orm_search_fields = []
        queryset_by_func_ids = []
        for search_field in search_fields:
            orm_lookup = self._construct_search(str(search_field))
            if orm_lookup is not None:
                orm_search_fields.append(search_field)
                orm_lookups.append(orm_lookup)
            else:
                self._filter_by_external_func(queryset_by_func_ids, search_field[1:], queryset, search_terms)

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        if queryset_by_func_ids:
            queryset |= base.filter(id__in=queryset_by_func_ids)

        if self.must_call_distinct(queryset, orm_search_fields):
            # Filtering against a many-to-many field requires us to
            # call queryset.distinct() in order to avoid duplicate items
            # in the resulting queryset.
            # We try to avoid this if possible, for performance reasons.
            queryset = distinct(queryset, base)

        return queryset


class OrderingFilter(BaseOrderingFilter):
    ordering_param = 'ordering'

    def filter_queryset(self, request, queryset, view):
        return super(OrderingFilter, self).filter_queryset(request, queryset, view)


    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.
        """
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = self._remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering
        # No ordering was included, or all the ordering fields were invalid
        return self._get_default_ordering(view)

    def _get_default_ordering(self, view):
        ordering = getattr(view, 'ordering_default', None)
        if isinstance(ordering, str):
            return (ordering,)
        return ordering

    def _remove_invalid_fields(self, queryset, fields, view, request):
        """
        [예시]
        - ordering = [('field1', Length('name')), 'field2', 'field3']
        - fields = ['field2', 'field1', 'field4']
        이라면 ['field2', Length('name')] 을 return한다.
        """
        valid_fields = [item for item in self.get_valid_fields(queryset, view, {'request': request})]
        ordering = []
        for term in fields:
            for valid_field in valid_fields:
                if term.lstrip('-') == valid_field[0] and ORDER_PATTERN.match(term):
                    ordering.append(term if valid_field[0] == valid_field[1] else valid_field[1])

        return ordering

    def get_schema_fields(self, view):
        """
        ordering가 없이 ordering_default만 있는경우 swagger에 보이지 않는다
        """
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'

        if getattr(view, 'ordering', None) is None:
            return []

        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=force_str(self.ordering_description)
                )
            )
        ]


class CategoryFilter(BaseFilterBackend):
    filter_param = 'category'
    def filter_queryset(self, request, queryset, view):
        category_param = request.GET.get('category')
        if not category_param:
            return queryset
        try:
            queryset = queryset.filter(category=category_param)
        except Exception as e:
            pass

        return queryset

    def get_schema_fields(self, view):
        """
        swagger에 보여주기 위한 설정
        """
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'

        return [
            coreapi.Field(
                name=self.filter_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str('A category filter'),
                    description=force_str('Category filter')
                )
            )
        ]
