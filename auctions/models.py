from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal
from datetime import datetime 

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watchlist")


class Listing(models.Model):
    AVAILABLE_CATEGORIES = [
        ("HOME", "Home"),
        ("TOYS", "Toys"),
        ("CLOTHES", "Clothes"),
        ("ELECTRONICS", "Electronics"),
        ("FOOD", "Food"),
        ("GARDEN", "Garden"),
        ("BEAUTY", "Beauty"),
        ("BOOKS", "Books"),
        ("PETS", "Pets"),
        ("TOOLS", "Tools"),
    ]
    user_id = models.ForeignKey(User, on_delete = models.CASCADE, related_name="user_listings")
    title = models.CharField(max_length = 64)
    description = models.TextField()
    starting_bid = models.DecimalField(default=Decimal('0.00'), blank=True, max_digits=15, decimal_places=2)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete = models.SET_NULL, blank=True, null=True)
    listing_url = models.URLField(max_length = 200, blank=True)
    category = models.CharField(max_length = 64, choices=AVAILABLE_CATEGORIES)
    created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.id}: {self.title} is ${self.starting_bid}"


class Bid(models.Model):
    item_id = models.ForeignKey(Listing, related_name="item_bids", on_delete = models.CASCADE)
    user_id= models.ForeignKey(User, related_name="user_bids", on_delete = models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2) 
    created = models.DateTimeField(default=datetime.now, blank=True)
    

    def __str__(self):
        return f"{self.item_id} is ${self.amount} by {self.user_id}"



class Comment(models.Model):
    item_id = models.ForeignKey(Listing, related_name="listing_comments", on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name="comment_users", on_delete = models.PROTECT)
    comment_content = models.TextField()
    created = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return f"{self.id}: {self.item_id} by {self.user_id}"




