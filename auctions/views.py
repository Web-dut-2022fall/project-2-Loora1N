from django.contrib.auth import authenticate, get_user, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Biding, Comments, Listing, User, Watch


def index(request):
    context = {
        "listings": Listing.objects.filter(isActive=True),
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            
            if "next" in request.POST:
                next_url = request.POST["next"]
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if "next" in request.GET:
            next_url = request.GET["next"]
            context = {
                "next": next_url
            }
            return render(request, "auctions/login.html", context)
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
        Watch(watcher=user).save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        des = request.POST["description"]
        startBid = request.POST["startingBid"]
        current = startBid
        img = request.FILES.get("img")
        cate = request.POST["category"]
        user = get_user(request)

        item = Listing(title=title, description=des, startingBid=startBid,
                currentPrice=current, image=img, category=cate,
                listedBy=user, isActive=True)
        item.save()
        return HttpResponseRedirect(reverse("listing", args=(item.id,)))
    else:
        context = {
            "categories": Listing.CATEGORY_CHOICES
        }
        return render(request, "auctions/create.html", context)


@login_required(login_url='/login')
def listing(request, listId):
    item = Listing.objects.get(pk=listId)
    bidConut = item.biding_set.count()
    bidList = item.biding_set.all()
    commentList = item.comments_set.all()
    user = get_user(request)
    creater=False
    watched=False
    if item.listedBy == user:
        creater=True
    if user.watch.list.contains(item):
        watched=True
    watchCount = user.watch.list.count()
    context = {
        "item": item,
        "watched": watched,
        "watchCount": watchCount,
        "creater": creater,
        "bidCount": bidConut,
        "bids": bidList,
        "comments": commentList
    }
    return render(request, "auctions/listing.html", context)


@login_required(login_url='/login')
def watch(request, listId):
    item = Listing.objects.get(pk=listId)
    user = get_user(request)
    if request.POST["watch"]=="yes":
        user.watch.list.add(item)
    else:
        user.watch.list.remove(item)
    return HttpResponseRedirect(reverse("listing", args=(item.id,)))


@login_required(login_url='/login')
def watchlist(request):
    user = get_user(request)
    context = {
        "listings": user.watch.list.all(),
        "watchCount": user.watch.list.count()
    }
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url='/login')
def bid(request, listId):
    if request.method == "POST":
        item = Listing.objects.get(pk=listId)
        user = get_user(request)
        bid = float(request.POST["bid"])
        if not item.biding_set.count():
            if bid >= item.startingBid:
                pass
            else:
                context = {
                    "message": "Your bid must be at least as large as the starting bid!",
                    "id": item.id
                }
                return render(request, "auctions/error.html", context)
        else:
            if bid > item.currentPrice:
                pass
            else:
                context = {
                    "message": "Your bid must be higher than the current price!",
                    "id": item.id
                }
                return render(request, "auctions/error.html", context)

        b = Biding(bid=bid, bider=user, item=item)
        item.currentPrice = bid
        item.save()
        b.save()

        return HttpResponseRedirect(reverse("listing", args=(item.id,)))


@login_required(login_url='/login')
def close(request, listId):
    item = Listing.objects.get(pk=listId)
    if not item.biding_set.count():
        item.winner = get_user(request)
        item.isActive = False
        item.save()
    else:
        bidLog = item.biding_set.latest('bid')
        winner = bidLog.bider
        item.winner = winner
        item.isActive = False
        item.save()
    return HttpResponseRedirect(reverse("listing", args=(item.id,)))


@login_required(login_url='/login')
def comment(request, listId):
    item = Listing.objects.get(pk=listId)
    user = get_user(request)
    comment = request.POST["comment"]
    Comments(comment=comment, commenter=user, item=item).save()
    return HttpResponseRedirect(reverse("listing", args=(item.id,)))

def categories(request):
    context = {
        'categories': Listing.CATEGORY_CHOICES
    }
    return render(request, "auctions/categories.html", context)


def category(request, cateID):
    
    context = {
        'listings': Listing.objects.filter(category=cateID)
    }
    return render(request, "auctions/category.html", context)
