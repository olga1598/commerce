from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Listing, User, Comment, Bid
from django.views.generic import CreateView
from django import forms
from django.db.models import Max

from .models import User


class NewListingForm(forms.Form):
    CHOICES = (('', '----'),
        ("HOME", "Home"),
        ("TOYS", "Toys"),
        ("CLOTHES", "Clothes"),
        ("ELECTRONICS", "Electronics"),
        ("FOOD", "Food"),
        ("GARDEN", "Garden"),
        ("BEAUTY", "Beauty"),
        ("BOOKS", "Books"),
        ("PETS", "Pets"),
        ("TOOLS", "Tools"),)
    title = forms.CharField(max_length=100, label="Title of new listing")
    description = forms.CharField(widget=forms.Textarea)
    start_bid = forms.DecimalField(decimal_places=2)
    image = forms.CharField(required=False)
    category = forms.ChoiceField(choices=CHOICES, required=False)

class ListingCreateView(CreateView):
    model = NewListingForm
    fields = ('title', 'description', 'start_bid', 'image', 'category')


class NewBidForm(forms.Form):
    place_bid = forms.DecimalField(decimal_places=2)


class NewCommentForm(forms.Form):
    comment = forms.CharField(max_length=200)


def index(request):
    # Get all the active listings
    listings = Listing.objects.all()
    # print(User.objects.get(id=1).first_name)
    # print(User.objects.get(id=1).watchlist)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def all_listings(request):
    # Get all the listings
    listings = Listing.objects.all()

    return render(request, "auctions/all_listings.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


 # Create new listing view    
@login_required
def create_new(request):
    # Login required - we have the user info via request.user
    print("Inside add")
    form = NewListingForm(request.POST)
    listing = Listing()
    if request.method == "POST":
        if form.is_valid():
            # Grabbing the values from the form
            # and assigning them to the properties of the model
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            image = form.cleaned_data["image"]
            category = form.cleaned_data["category"]
            listing.title = title
            listing.description = description
            listing.starting_bid = start_bid
            listing.user_id = request.user
            # If there is an image link
            if image != "":
                listing.listing_url = image
            else:
                listing.listing_url = "https://breakthrough.org/wp-content/uploads/2018/10/default-placeholder-image.png"
            # If there is a chosen category
            if category == '----':
                listing.category = ""
            else:
                listing.category = category
            # Save new listing
            listing.save()
            
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/create.html", {
            "form": NewListingForm()
        })


# Look for the listing details  
@login_required(login_url='login')
def listing_details(request, listing_id):
    #Template to hold the message if any
    message = ""

    # Counter for bids
    bids_count = 0

    # Current bidder
    current_bidder = ""

    # Pull out the current listing detailed data from DB
    listing = Listing.objects.get(id=listing_id)
   
    # Max bid for the moment
    max_bid = 0
    comment = NewCommentForm()

    # Check if the bidding form was submitted
    form = NewBidForm(request.POST)

    # When the bid is placed in the form
    # Pulling uot the last highest bid
    list_price = Listing.objects.get(id=listing_id).starting_bid
    if form.is_valid():
        user_bid = form.cleaned_data["place_bid"]

        bids = Bid.objects.filter(item_id=listing)
        if bids:
            # Pulling out the highest bid from the DB
            highest_bid = bids.order_by("amount").last().amount
            # Checking for the higher bid
            if user_bid <= highest_bid:
                message = "Your bid is too low"
            else:
                print("the bid is higher")
                # Save new bid            
                bid = Bid(item_id=listing, user_id=request.user, amount=user_bid)
                bid.save()
                max_bid = bid.amount
                print(max_bid)
                message = "You are the highest bidder"

        else: 
            if user_bid <= list_price:
                message = "Your bid is lower then the starting price."
            else:
                # Save new bid
                bid = Bid(item_id=listing, user_id=request.user, amount=user_bid)
                bid.save()
                max_bid = bid.amount
                print(max_bid)
                message = "You are the highest bidder!"

    # Check which max price for bidding to display
    bids = Bid.objects.filter(item_id=listing)
    if bids:
        # Pulling out the highest bid from the DB
        max_bid = bids.order_by("amount").last().amount
        bids_count = len(bids)
        current_bidder = bids.order_by("amount").last().user_id
        print(current_bidder)
        print(request.user)
    else:
        max_bid = listing.starting_bid

    # All the comments assosiated with this item
    all_comments = Comment.objects.filter(item_id=listing)

    # If any comments
    if (all_comments):
        any = True
    else:
        any = False
    bid = NewBidForm()
    in_watchlist = listing in request.user.watchlist.all()
    return render(request, "auctions/listings.html", {
        "listing": listing,
        "bid": bid,
        "user": request.user,
        "in_watchlist": in_watchlist,
        "comment": comment,
        "comments": all_comments,
        "any_comments": any,
        "message": message,
        "max_bid": max_bid,
        "bids": bids_count,
        "current_bidder": current_bidder
    })

@login_required
def toggle_watchlist(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    user = User.objects.get(id=request.user.id)

    # Checking if the listing in the authorized user wishlist
    in_watchlist = listing in request.user.watchlist.all()

    if in_watchlist:
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))


# Watchlist page
@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required
def comment(request, listing_id):
    form = NewCommentForm(request.POST)
    listing = Listing.objects.get(id=listing_id)
    if request.method == "POST":
        if form.is_valid():
            print(form.cleaned_data["comment"])
            print(listing_id)
            print(request.user)
            comment = Comment(item_id=listing, user_id=request.user, comment_content=form.cleaned_data["comment"])
            comment.save()

    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))

@login_required
def add_bid(request, listing_id):
    print("inside bid")
    form = NewBidForm(request.POST)
    saved_bid = Listing.objects.get(id=listing_id).starting_bid
    print(form)

    user_bid = form.cleaned_data["place_bid"]
    print(user_bid)
    
    if user_bid <= saved_bid:
        message = "Your bid is too low"
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "bid": bid,
            "user": listing.user_id,
            "in_watchlist": in_watchlist,
            "comment": comment,
            "comments": all_comments,
            "any_comments": any
        })


    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))


# Display all the categories
@login_required(login_url='login')
def categories(request):
    categories = Listing.objects.order_by("category").values_list("category", flat=True).distinct()
    print(categories)
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


# Display a list of items in certain chosen category
@login_required(login_url='login')
def category_listing(request, category):
    print(category)
    category_list = Listing.objects.filter(category=category, active=True)
    print(category_list)
    return render(request, "auctions/index.html", {
        "listings": category_list,
        "category_name": category
    })


# Close auction
@login_required(login_url='login')
def close_auction(request, listing_id):
    # Find the listing by id
    listing_to_close = Listing.objects.get(id=listing_id)
    # Find all the bids for the listing 
    # Sort them in increasing order
    # Pick the very last one from the list
    winner = Bid.objects.filter(item_id=listing_id).order_by('amount').last()
    if winner:
        listing_to_close.winner = winner.user_id
    listing_to_close.active = False
    listing_to_close.save()
    
    return HttpResponseRedirect(reverse("listing_details", args=(listing_id,)))




