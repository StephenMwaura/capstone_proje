from django.shortcuts import render
from .models import Movie , Moviereview, Comment
from rest_framework.permissions import IsAuthenticated , AllowAny,IsAdminUser
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics
# Create your views here.
from rest_framework import viewsets
from .serializers import MoviereviewSerializer,MovieSerializer,UserSerializer,CommentSerializer,ProfileSerializer, UserRegistrationSerializer
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.db import models # allows the MostlikedReviewviewset to count the most liked review
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthorOrReadOnly

class UserRegistrationView(generics.CreateAPIView): #Provides a post method for handling registration
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            # Create a token for the newly created user
            token, created = Token.objects.get_or_create(user=serializer.instance)
            return Response({
                "user": serializer.data,
                "token": token.key,
            }, status=status.HTTP_201_CREATED)
        
        # Return error response if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # access only for admin users

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    

        

    def perform_create(self, serializer):
        serializer.save()

class MovieReviewViewSet(viewsets.ModelViewSet):
    queryset = Moviereview.objects.all()
    serializer_class = MoviereviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['movie__title'] # allows users to search movie review by movie titles and rating
    filterset_fields = ['movie__title','rating'] # allowers filtering by movie title and rating
    ordering_fields = ['rating','created_date'] # allows users to sort movie reviews by rating and date created

  

    def perform_create(self , serializer): # creating a moviereview
        serializer.save(user=self.request.user)

    @action(detail=True,methods=['post'],permission_classes=[IsAuthenticated])
    def like(self, request,pk=None):
        review = self.get_object()
        user = request.user

        if user in review.likes.all(): # check if user the user has already liked this review
            review.likes.remove(user) # if user has already liked this review then the user will be removed
            return Response ({'status': 'review unliked'},status=status.HTTP_200_OK)
        else:
            review.likes.add(user) # if the user has not liked this review the user is added to the list
            return  Response({'status': 'liked'},status=status.HTTP_200_OK)
        
    
class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get_object(self):
        return self.request.user.profile # gets the current authenticated user
    

    

class MostlikedReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MoviereviewSerializer

    def get_queryset(self):
        return Moviereview.objects.annotate(likes_count=models.Count('likes')).order_by('-likes_count')[:5] # gets the 5 most liked reviews
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer): # creating a comment
        serializer.save(user=self.request.user)

