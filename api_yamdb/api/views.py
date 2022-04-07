from urllib import request
import uuid

from rest_framework import status, viewsets

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from .permissions import (
    CustomIsAdmin,
    IsAdminOrReadOnly
)
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UsersSerializer
)

from composition.models import Titles, Genres, Categories, Author
from reviews.models import Reviews, User
from .serializers import (
    TitlesSerializer,
    AuthorSerializer,
    CategoriesSerializer,
    GenresSerializer,
    ReviewsSerializer,
    CommentsSerializer
)


class SignUp(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_class = [AllowAny]

    # def get_queryset(self):
    #    user = get_object_or_404(User, username=self.request.user.username)
    #    queryset = User.objects.all().filter(username=user)
    #    print(1111111111, user, queryset)
    #    return queryset

    def perform_create(self, serializer):
        confirmation_code = str(uuid.uuid4())
        # username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        if email not in User.objects.all():
            print(email, self.request.user)
            serializer.save(confirmation_code=confirmation_code)
        return send_mail(
            'Код подверждения',
            confirmation_code,
            email,
            ['admin@email.com'],
            fail_silently=False
        )


class APIToken(APIView):
    queryset = User.objects.all()
    serializer_class = TokenSerializer
    permission_class = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        confirmation_code = serializer.data['confirmation_code']
        user_base = get_object_or_404(User, username=username)
        if confirmation_code == user_base.confirmation_code:
            token = str(AccessToken.for_user(user_base))
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminUser,)
    permission_classes = (CustomIsAdmin, )
    lookup_field = 'username'


class UsernameViewSet(viewsets.ModelViewSet):
    # queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (AllowAny,)
    permission_classes = (CustomIsAdmin, )

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print(self.kwargs.get('username'), user.email)
        queryset = User.objects.all().filter(username=user)
        return queryset


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [
        IsAdminOrReadOnly
    ]


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    permission_classes = [
        IsAdminOrReadOnly
    ]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        id = self.kwargs.get('id')
        title = get_object_or_404(Titles, id=id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        id = self.kwargs.get('id')
        a=input(f'title id === {id}')
        title = get_object_or_404(Titles, id=id)
        serializer.save(title=title, author=request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id)
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Reviews, id=review_id)
        serializer.save(review=review)
