from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    MeAPI,
    SignUpAPI,
    TokenAPI,
    UsersViewSet,
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    AuthorViewSet,
    ReviewViewSet,
    CommentViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register('users', UsersViewSet)
router.register('titles', TitlesViewSet)
router.register('author', AuthorViewSet)
router.register('genres', GenresViewSet, basename='genres')
router.register('categories', CategoriesViewSet, basename='categories')
router.register(
    r'titles/(?P<id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)

router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/'
    '(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/auth/token/', TokenAPI.as_view()),
    path('v1/users/me/', MeAPI.as_view()),
    path('v1/auth/signup/', SignUpAPI.as_view()),
    path('v1/', include(router.urls)),
]
