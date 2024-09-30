from .models import Moviereview , Movie, Comment ,Profile
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True,required=True)
     password2 = serializers.CharField(write_only=True,required=True)
     email = serializers.EmailField(required=True)
     class Meta:
          model = User
          fields = ['username', 'email', 'password','password2']

     def validate(self, data):
                if data['password']!=data['password2']:
                    raise serializers.ValidationError("Passwords must match")
                return data
          
     def validate_username(self, value):
               if User.objects.filter(username=value).exists():
                    raise serializers.ValidationError("Username already exists")
               return value
     def validate_email(self, value):
               if User.objects.filter(email__iexact=value).exists():
                    raise serializers.ValidationError("Email already exists")
               return value
               
     def create(self, validated_data): # a function for creating the user and validating
                user=User(
                    username = validated_data['username'],
                    email=validated_data['email'],
               
                )
                user.set_password(validated_data['password'])
                user.save()
                Profile.objects.create(user=user)
                Token.objects.create(user=user)
                return user
          
class UserSerializer(serializers.ModelSerializer):
     class Meta:
          model = User
          fields = ['id','username', 'email']



class CommentSerializer(serializers.ModelSerializer):
     movie_title = serializers.CharField(source='review.movie.title',read_only=True)
     class Meta:
          model = Comment
          fields = ['id','content', 'created_date','review','movie_title']
          read_only_fields = ['id','created_date']


class MoviereviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField() # count the number of likes a movie review has
    is_liked = serializers.SerializerMethodField() # show if the current user has liked this movie
    movie_name= serializers.CharField(source='movie_title',read_only = True) # displays the movie title as a string field
    comments = CommentSerializer(many=True,read_only=True) # displays
    class Meta:
        model = Moviereview
        fields = ['id','movie', 'review_content' ,'rating', 'created_date', 'user','likes_count','is_liked','comments','movie_name']
        read_only_fields = ['likes_count', 'is_liked','user', 'created_date'] # these fields are not meant to be modified by the user

    def create(self, validated_data):
         movie_title = validated_data.pop('movie')
         try:
             movie = Movie.objects.get(title=movie_title)
         except Movie.DoesNotExist:
               raise serializers.ValidationError(f"Movie with title {movie_title} does not exist")
         review = Moviereview.objects.create(movie=movie,**validated_data) # creates a new movie review and returns it
         return review

    def get_likes_count(self, obj):
         return obj.likes.count()
    
    def get_is_liked(self, obj):
         user = self.context.get('request').user
         return user in obj.likes.all() #checks if the current user has liked this movie review
    def validate_rating(self,value):
         if value <1 or value >5:
                raise serializers.ValidationError("Rating must be between 1 and 5")
         return value
    
            



class MovieSerializer(serializers.ModelSerializer):
   reviews = MoviereviewSerializer(many=True,read_only=True)
   class Meta:
          model = Movie
          fields = ['id','title', 'description', 'release_date','reviews']
        
class ProfileSerializer(serializers.ModelSerializer):
     user = UserSerializer(read_only=True)
     class Meta:
          model = Profile
          fields = ['user','bio','location']


