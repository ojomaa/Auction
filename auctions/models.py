from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    def __str__(self):
        return f"user: {self.username}"

class Category(models.Model):
    name = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title= models.CharField(max_length= 100)
    description= models.TextField(max_length= 400)
    starting_bid= models.DecimalField(decimal_places=2, max_digits=10)
    image= models.ImageField()
    start_time= models.TimeField(auto_now_add=True)
    end_time= models.TimeField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name= "listing_user")
    category= models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "category")
    watchlist = models.ManyToManyField(User,related_name="watchlist")
    status= models.BooleanField(default=True)

    def __str__(self):
        return f" Auction# {self.id}: {self.title}"

class Bid(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE, related_name= "bid_user")
    price= models.DecimalField(decimal_places=2, max_digits= 10)
    listing= models.ForeignKey(Listing, on_delete = models.CASCADE, related_name= "bid_listing")

    def __str__(self):
        return f"Price for {self.listing}: ${self.price} ({self.user})"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name= "comment_user")
    title = models.CharField(max_length=100)
    description = models. TextField()
    listing= models.ForeignKey(Listing, on_delete = models.CASCADE, related_name= "comment_listing")

    def __str__(self):
        return f"User {self.user} posted a comment on {self.listing} with the title {self.title}"
