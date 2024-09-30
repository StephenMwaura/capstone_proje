from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=400)
    release_date = models.DateField()
 
    def __str__(self):
        return self.title

class Moviereview(models.Model):
    movie = models.ForeignKey(Movie , on_delete=models.CASCADE, related_name='reviews') # allows multiple reviews for a single movie 
    review_content = models.CharField(max_length=300)
    rating = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reviews')
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User ,related_name='liked_views', blank=True) # this is a many to many relationship to  the user model allowing multiple users to like  the reviews

    def __str__(self):
        return f"Review by {self.user.username} for {self.movie.title}"
    
    def total_likes(self):
        return self.likes.count()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=30, blank=True)
    
    def __str__(self):
        return self.user.username
class Comment(models.Model):
    review = models.ForeignKey(Moviereview, on_delete=models.CASCADE ,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.movie.title}"