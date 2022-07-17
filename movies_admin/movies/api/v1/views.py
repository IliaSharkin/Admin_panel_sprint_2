from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from movies.models import Filmwork


class MoviesListApi(BaseListView):
    model = Filmwork
    http_method_names = ['get']  # Список методов, которые реализует обработчик
    paginate_by = 50

    def get_queryset(self):
        values = ("id", "title", "description", "creation_date", "rating", "type")
        return Filmwork.objects.values(*values).annotate(
            genres=ArrayAgg(
                "genres__name",
                distinct=True,
            ),
            actors=ArrayAgg(
                "personfilmwork__person__full_name",
                filter=Q(personfilmwork__role="actor"),
                distinct=True,
            ),
            writers=ArrayAgg(
                "personfilmwork__person__full_name",
                filter=Q(personfilmwork__role="writer"),
                distinct=True,
            ),
            directors=ArrayAgg(
                "personfilmwork__person__full_name",
                filter=Q(personfilmwork__role="director"),
                distinct=True,
            ),
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        page_size = self.paginate_by
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'results': list(queryset),
        }

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
