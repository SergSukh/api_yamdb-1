from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    TitlesViewSet,
    GenresViewSet,
    CategoriesViewSet,
    AuthorViewSet,
    ReviewViewSet,
    CommentViewSet
)

router = DefaultRouter()
router.register('titles', TitlesViewSet)
router.register('genres', GenresViewSet)
router.register('categories', CategoriesViewSet)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
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
    path('v1/', include(router.urls)),
]
