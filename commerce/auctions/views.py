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

    newbid = request.POST["newbid"]
    allbids =  comment.objects.filter(post_id=post_id)
    if len(allbids)=0:
        comments = comment.objects.filter(post_id=post_id)
        post = Post.objects.get(id=post_id)
        if newbid <= post.starting_bid:
            message = "enter new bid bigger than the current"
            context = {
                'message':message,
                'post' :post ,
                'comments' :comments
            }
            return render(request,'auctions/post.html',context)


            
        



    new_bid = bid()
    new_bid.post_id = Post.objects.get(id=post_id)
    new_bid.user_id = request.user
    new_bid.bid = newbid
    new_bid.save()
    


def watch_list(request):
    pass


def categories(request):
    pass
    

def create_list(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user_id = request.user
            new_form.save()
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

    context = {
        'post' :post ,
        'comments' :comments
    }

    return render(request,'auctions/post.html',context)
