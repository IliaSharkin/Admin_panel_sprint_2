import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("name"), max_length=200)
    description = models.CharField(_("description"), max_length=50, null=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        ordering = ('-name',)
        db_table = 'content\".\"genre'

    def __str__(self):
        return self.name


class Person(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(_("full_name"), max_length=200)
    birth_date = models.DateField(
        _("birth_date"), auto_now=False, auto_now_add=False, null=True
    )

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        ordering = ('-full_name',)
        db_table = 'content\".\"person'

    def __str__(self):
        return self.full_name


class Filmwork(TimeStampedModel):

    class FilmworkType(models.TextChoices):
        MOVIE = "movie", _("movie")
        TV_SHOW = "tv_show", _("TV Show")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"), blank=True, null=True)
    creation_date = models.DateField(
        _("creation_date"), auto_now=False, auto_now_add=False, null=True
    )
    certificate = models.TextField(_("certificate"), blank=True, null=True)
    file_path = models.FileField(
        _("file"), upload_to="film_works/", max_length=200, null=True
    )
    rating = models.FloatField(
        _("rating"), validators=[MinValueValidator(0), MaxValueValidator(10)],
        blank=True, null=True
    )
    type = models.CharField(_("type"), max_length=20, choices=FilmworkType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        ordering = ('-title',)
        db_table = 'content\".\"film_work'

    def __str__(self):
        return self.title


class GenreFilmwork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        "Genre", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = [
            UniqueConstraint(fields=['film_work', 'genre'], name='film_work_genre_cnst')
        ]
        indexes = [
            models.Index(fields=['film_work', 'genre'], name='film_work_genre_idx'),
        ]


class PersonRole(models.TextChoices):
    screenwriter = 'screenwriter', _('screenwriter')
    actor = 'actor', _('actor')
    director = 'director', _('director')


class PersonFilmwork(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    film_work = models.ForeignKey(
        "Filmwork", on_delete=models.CASCADE
    )
    person = models.ForeignKey(
        "Person", on_delete=models.CASCADE
    )
    role = models.CharField(_("role"), max_length=50, choices=PersonRole.choices)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=False)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = [
            UniqueConstraint(fields=['film_work', 'person'], name='film_work_person_cnst')
        ]
        indexes = [
            models.Index(fields=['film_work', 'person'], name='film_worlk_person_idx'),
        ]
