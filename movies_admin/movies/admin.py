from django.contrib import admin
from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class PersonRoleInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0


class FilmWorkGanreInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):



    list_display = (
        "title",
        "type",
        "creation_date",
        "get_genres",
        "rating",
    )

    list_prefetch_related = ('genres',)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ',  '.join([genre.name for genre in obj.genres.all()])

    search_fields = ('title', 'description', 'id',)

    list_filter = ('type',)

    get_genres.short_description = 'Жанры фильма'

    fields = (
        "title",
        "type",
        "description",
        "creation_date",
        "certificate",
        "file_path",
        "rating",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

    fields = ("name", "description")

    inlines = [FilmWorkGanreInline]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("full_name", "birth_date")

    fields = ("full_name", "birth_date")

    inlines = [PersonRoleInline]
