from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SignUp,
    APIToken,
    UsersViewSet,
    UsernameViewSet,
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    AuthorViewSet,
    ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()

app_name = 'api'
router.register('auth/signup', SignUp, basename='signup')
router.register(
    r'users/(?P<username>[\w.@+-]+)',
    UsernameViewSet,
    basename='users'
)
router.register('users', UsersViewSet)
router.register('titles', TitlesViewSet)
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register(
    r'titles/(?P<id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('author', AuthorViewSet)

urlpatterns = [
    path('v1/auth/token/', APIToken.as_view()),
    path('v1/', include(router.urls)),
]
