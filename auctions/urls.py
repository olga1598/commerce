from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_new, name="create_new"),
    path("<int:listing_id>", views.listing_details, name="listing_details"),
    path("toggle_watchlist/<str:listing_id>", views.toggle_watchlist, name="toggle_watchlist"),
    path("comment/<str:listing_id>", views.comment, name="comment"),
    path("add_bid/<str:listing_id>", views.add_bid, name="add_bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listing/<str:category>", views.category_listing, name="category_listing"),
    path("close/<str:listing_id>", views.close_auction, name="close_auction")
]
