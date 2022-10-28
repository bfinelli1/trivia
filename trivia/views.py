from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Group
from django.http import JsonResponse
import requests


# Create your views here.
def index(request):
    return render(request, 'trivia/index.html', {
        "groups" : Group.objects.all(),
        "profile" : request.user
    })

def getGroups(request):
    groups = Group.objects.all()
    return JsonResponse([group.serialize() for group in groups], safe=False)


def random(request):
    return render(request, 'trivia/index.html')

def newgroup(request):
    if request.method == "POST":
        name = request.POST['group']
        myGroup = Group(groupname=name)
        myGroup.save()
        myGroup.participants.add(request.user)
        user = request.user
        qlistlength = 0
        while qlistlength<10: #check if there are too few qs in the category
            response = requests.get("https://jservice.io/api/random")
            categoryid = response.json()[0]['category_id']
            categoryname = response.json()[0]['category']['title']
            questionlist = requests.get(f"https://jservice.io/api/clues?category={categoryid}")
            print(f"{categoryid} amount in category: {len(questionlist.json())}")
            qlistlength = len(questionlist.json())
        myGroup.categoryid = categoryid
        myGroup.categoryname = categoryname
        myGroup.save()
    return HttpResponseRedirect(reverse("index"))

def joingroup(request, groupid):
    # user = request.user
    # if user.group:
    #     print(user.group.groupname)
    #     if user.group.num_participants > 0:
    #         user.group.num_participants = user.group.num_participants - 1
    #         user.group.save()
    group = Group.objects.get(pk=groupid)
    # print(group.groupname)
    # user.group = group
    # user.save()
    # group.num_participants = group.num_participants + 1
    # print(group.num_participants)
    # group.save()
    return render(request, "trivia/lobby.html", {
        "groupid" : groupid,
        "groupname" : group.groupname,
        "categoryname" : group.categoryname,
        "categoryid" : group.categoryid
    })

def lobby(request):
    return HttpResponseRedirect(reverse("index"))

def question(request):
    if request.method == "POST":
        choice = request.POST['choice']
        print(choice)
        return render(request, 'trivia/question.html', {
        "category": choice
        })

def delete(request, groupid):
    if Group.objects.filter(pk=groupid).exists():
        Group.objects.get(pk=groupid).delete()
    groups = Group.objects.all()
    
    return JsonResponse([group.serialize() for group in groups], safe=False)


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
            return render(
                request,
                "trivia/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "trivia/login.html")


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
            return render(request, "trivia/register.html",
                          {"message": "Passwords must match."})

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "trivia/register.html",
                          {"message": "Username already taken."})
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "trivia/register.html")
