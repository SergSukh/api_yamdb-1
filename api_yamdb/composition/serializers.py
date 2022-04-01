"""Обработка запросов и ответов к базе произведения."""

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import datetime as dt

from .models import GenreTitle, Titles, Genres, Categories, Author


class AuthorSerializer(serializers.ModelSerializer):
    """Для отображения по информации автор (для расширения)."""

    titles = serializers.SlugRelatedField(
        slug_field='title',
        many=True,
        allow_null=True,
        read_only=True
    )

    class Meta:
        model = Author
        fields = ('slug', 'titles',)


class GenresSerializer(serializers.ModelSerializer):
    """Жанры, описание."""

    class Meta:
        model = Genres
        fields = ('genre',)


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории, описание."""

    class Meta:
        model = Categories
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    """Основной метод получения информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Categories.objects.all()
    )
    genres = GenresSerializer(many=True, required=False)
    author = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Author.objects.all()
    )
    year = serializers.SerializerMethodField()

    class Meta:
        fields = ('pk', 'title', 'author', 'year', 'category', 'genres')
        model = Titles
        validators = [
            UniqueTogetherValidator(
                queryset=Titles.objects.all(),
                fields=('title', 'author', 'category')
            )
        ]

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('ПРоверьте год')
        return value

    def create(self, validated_data):
        """Определяем наличие жанров и прописываем."""
        if 'genres' not in self.initial_data:
            title = Titles.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genres')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genres.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)

        return title
