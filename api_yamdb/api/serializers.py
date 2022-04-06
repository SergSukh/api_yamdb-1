"""Обработка запросов и ответов к базе произведения."""

from turtle import title
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

import datetime as dt

from statistics import mean

from composition.models import (
    GenreTitle,
    Titles,
    Genres,
    Categories,
    Author
)
from review.models import (Reviews, Comment)


class AuthorSerializer(serializers.ModelSerializer):
    """Для отображения по информации автор (для расширения)."""

    titles = serializers.StringRelatedField(
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
        fields = ('slug', 'category')


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
        queryset=Author.objects.all(),
        required=False
    )
    reviews = serializers.StringRelatedField(
        many=True,
        read_only=True,
        allow_null=True
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        # '__all__'
        fields = ('pk', 'name', 'author', 'year', 'description', 'category', 'genres', 'reviews', 'rating')
        model = Titles
        validators = [
            UniqueTogetherValidator(
                queryset=Titles.objects.all(),
                fields=('name', 'year', 'category')
            )
        ]

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('ПРоверьте год')
        return value
    
    def get_rating(self, obj):
        review = obj.reviews.all()
        rating = review.count()
        return rating

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


class ReviewsSerializer(serializers.ModelSerializer):
    """Ревью для произведений"""
    author =serializers.SlugRelatedField(
        slug_field='slug',
        queryset = Author.objects.all()
    )
    title = serializers.StringRelatedField(
        many=False,
        read_only=True
    )
    class Meta:
        fields = '__all__'
        model = Reviews
        read_only_fields = ['title']
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(),
                fields=('text', 'author', 'title')
            )
        ]

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверьте оценку')
        return value


class CommentsSerializer(serializers.ModelSerializer):
    """Комментарии на отзывы"""
    class Meta:
        fields = '__all__'
        model = Comment
        validators = [
            UniqueTogetherValidator(
                queryset=Comment.objects.all(),
                fields=('text', 'author', 'review')
            )
        ]
