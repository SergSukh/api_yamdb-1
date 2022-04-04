from rest_framework import viewsets, permissions

from .models import Titles, Genres, Categories, Author
from .permissions import IsAdminOrReadOnly
from .serializers import (
    TitlesSerializer,
    AuthorSerializer,
    CategoriesSerializer,
    GenresSerializer
)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = [IsAdminOrReadOnly]


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    # permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    # permission_classes = [IsAdminOrReadOnly]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
