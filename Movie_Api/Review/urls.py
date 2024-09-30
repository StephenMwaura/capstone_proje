from django.urls import path,include
from .views import MovieViewSet, MovieReviewViewSet ,UserListViewSet, ProfileView, MostlikedReviewViewSet, CommentViewSet ,UserRegistrationView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'moviereviews',MovieReviewViewSet, basename='moviereviews')
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'mostliked', MostlikedReviewViewSet, basename='mostliked')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'userlist', UserListViewSet, basename='user_list')
urlpatterns = [
    # path('register/', UserView.as_view(), name='register'),
    path('profile/',ProfileView.as_view(), name='profile'),
    path('register/',UserRegistrationView.as_view(), name='register'),
    path('', include(router.urls))
]