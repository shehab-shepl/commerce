from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render ,redirect
from django.urls import reverse

from .models import *

from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','img','category','active','seller','starting_bid']



def index(request):
    all_posts = Post.objects.all()
    context = {
        'all_posts':all_posts,
    }
    return render(request,'auctions/index.html',context)


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




def add_comment(request,post_id):
    
        new_comment = comment()
        new_comment.comment = request.POST["newcomment"]
        new_comment.post_id = Post.objects.get(id=post_id)
        new_comment.user_id = request.user
        new_comment.save()
        post = Post.objects.get(id=post_id)
        comments = comment.objects.filter(post_id=post_id)

        context = {
            'post' :post ,
            'comments' :comments
        }

        return render(request,'auctions/post.html',context)





def add_bid(request,post_id):

    post = Post.objects.get(id=post_id)
    comments = comment.objects.filter(post_id=post_id)
    current_bid =  bid.objects.get(post_id=post_id)
    
    newbid = request.POST["newbid"]
    if int((current_bid).bid) < int(newbid):
        current_bid.delete()
        new_bid = bid()
        new_bid.bid = newbid
        new_bid.post_id = Post.objects.get(id=post_id)
        new_bid.user_id = request.user
        new_bid.save() 
        updated_bid = bid.objects.get(post_id=post_id)
        message = "your bid saved"
        msg_type = "success"
    else:
        message = "enter new bid bigger than the current"
        msg_type= "danger"
        updated_bid = current_bid
    context = {
        "msg_type":msg_type ,
        'message':message,
        'post' :post ,
        'comments' :comments,
        'currentbid' : updated_bid
    }
    return render(request,'auctions/post.html',context)





def addtowatchlist(request ,post_id):
    added = Watchlist.objects.filter(post_id = post_id, user_id = request.user)
    if added:
        added.delete()
    else:
        new_watch= Watchlist()
        new_watch.user_id = request.user
        new_watch.post_id = Post.objects.get(id=post_id)
        new_watch.save()
    return redirect ('/')




def watch_list(request):
    watchlist = Watchlist.objects.filter(user_id = request.user)
    context = {
        'watchlist' : watchlist
    }
    #return redirect ('/')
    return render(request,'auctions/watchlist.html',context)



def categories(request):
    categories = ["Fashion","Tools","Toys","Electronics","Accessories","Books"]
    context = {
        'categories' : categories
    }
    #return redirect ('/')
    return render(request,'auctions/categories.html',context)


def category(request,category):

    all_posts = Post.objects.filter(category = category)

    context = {
        'all_posts' : all_posts
    }
    
    return render(request,'auctions/index.html',context)

def create_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user_id = request.user
            new_form.save()

        current_bid = bid()
        current_bid.bid = new_form.starting_bid
        current_bid.post_id = new_form
        current_bid.user_id = request.user
        current_bid.save()
        return redirect ('/')

    else:
        form = PostForm()
    context = {
        "form":form,
    }
    return render(request,'auctions/create.html',context)


def post(request, id):
    post = Post.objects.get(id=id)
    comments = comment.objects.filter(post_id=id)
    currentbid = bid.objects.get(post_id=id)
    
    added = Watchlist.objects.filter(post_id = id, user_id = request.user)
    context = {
        'post' :post ,
        'comments' :comments,
        'currentbid' : currentbid,
        'added':added
    }

    return render(request,'auctions/post.html',context)
