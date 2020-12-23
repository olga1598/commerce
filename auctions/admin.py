from django.contrib import admin

from .models import User, Bid, Comment, Listing


class ListingAdmin(admin.ModelAdmin):
    list_display =("id", "title", "starting_bid", "listing_url", "category")


# Register your models here.
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Listing)
