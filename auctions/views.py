from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(), 
        "category": Category.objects.all()
    })

def listing(request, listing_id):
    listing= Listing.objects.get(pk= listing_id)
    watchlistStatus= request.user in listing.watchlist.all()
    bid=Bid.objects.filter(listing=listing)
    comment= Comment.objects.filter(listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlistStatus": watchlistStatus,
        "bid": bid,
        "comment":comment,
    })

def watchlist(request):
    user= request.user
    listing= user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "listing": listing,
        "user": user
    })

def addWatchlist(request, listing_id):
    user = request.user
    listing= Listing.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))

def removeWatchlist(request, listing_id):
    user = request.user
    listing= Listing.objects.get(pk=listing_id)
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=[listing.id]))

def bid(request, listing_id):
    if request.method == 'POST':

        bid_price = request.POST['price']
        user = request.user
        listing= Listing.objects.get(pk=listing_id)

        try:
            bid=Bid.objects.filter(listing=listing).latest('id')
        except Bid.DoesNotExist:
            bid= Bid(user=listing.user, listing=listing, price=0)

        if Bid.user != user and bid.price < float(bid_price) and float(bid_price) >= listing.starting_bid  :
            
            submit_bid= Bid(
                user=user,
                price=bid_price,
                listing=listing
            )
            submit_bid.save()
            messages.success(request, "Your bid is successful!")
        else:
            messages.error(request, "Your bid is not high enough. Place a higher bid and try again.")

        
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

def close_listing(request, listing_id):
    if request.method == 'POST':
        listing=Listing.objects.get(pk=listing_id)
        listing.status = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))
    
def comment(request, listing_id):
    if request.method == 'POST':
        listing=Listing.objects.get(pk=listing_id)
        user=request.user
        title= request.POST['title']
        comment= request.POST['comment']
        
        submit_comment= Comment(
            user=user,
            listing=listing,
            title=title,
            description=comment,
        )
        
        submit_comment.save()
        return HttpResponseRedirect(reverse("listing", args=[listing.id]))

def create(request):
    if request.method == 'POST':

        
        title = request.POST['title']
        description=request.POST['description']
        price=request.POST['price']
        image=request.POST['image']
        category=request.POST['category']
        end_time=request.POST['end_time']
        user= request.user
        categorydata=Category.objects.get(name= category)

        
        list= Listing(
            title=title,
            description= description,
            image=image,
            user=user,
            starting_bid=float(price),
            end_time=end_time,
            category=categorydata
        )

        
        list.save()

        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create_listing.html", {
            "category": Category.objects.all()
        })
    
def categories(request):
    return render(request, "auctions/categories.html", {
        "category": Category.objects.all()
    })

def category(request, category_name):
    
    category= Category.objects.get(pk =category_name)

    listings= category.category.all()
    return render(request, "auctions/category.html", {
        "category": category,
        "listings": listings,

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
 