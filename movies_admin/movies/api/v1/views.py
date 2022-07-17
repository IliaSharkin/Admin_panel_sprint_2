from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from movies.models import Filmwork


class MoviesApiMixin:
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
    
    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)
    

class MoviesListApi(MoviesApiMixin, BaseListView):

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, *, object_list=None, **kwargs):
        pk = self.get_object()["id"]
        context = super().get_context_data(kwargs={"pk": pk})
        context = context["object"]
        
        return context
