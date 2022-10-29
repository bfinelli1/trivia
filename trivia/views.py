from curses.ascii import US
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Group, Scores
from django.http import JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt



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
        categoryid=0
        count=0

        categoryids = Group.objects.all().values_list('categoryid', flat=True)
        print(categoryids)
        qlistlength = 0
        while qlistlength<20 or (categoryid in categoryids) and count < 5: #check if there are too few qs in the category
            response = requests.get("https://jservice.io/api/random")
            categoryid = response.json()[0]['category_id']
            categoryname = response.json()[0]['category']['title']
            questionlist = requests.get(f"https://jservice.io/api/clues?category={categoryid}")
            print(f"{categoryid} amount in category: {len(questionlist.json())}")
            qlistlength = len(questionlist.json())
            count +=1
        if count >=5:
            print("didnt find a category")
            return HttpResponseRedirect(reverse("index"))
        else:
            myGroup = Group()
            myGroup.save()
            myGroup.categoryid = categoryid
            myGroup.categoryname = categoryname
            myGroup.save()
    return HttpResponseRedirect(reverse("index"))

def joingroup(request, groupid):
    group = Group.objects.get(pk=groupid)
    scores = Scores.objects.filter(group_id=groupid).all()
    return render(request, "trivia/lobby.html", {
        "groupid" : groupid,
        "categoryname" : group.categoryname,
        "categoryid" : group.categoryid,
        "scores" : scores
    })

def lobby(request):
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
def score(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("number"), data.get("gameid"))
        if data.get("number") is not None:
            score = Scores.objects.get(pk=int(data.get("gameid")))
            score.numscore = score.numscore+int(data.get("number"))
            score.numcompleted = score.numcompleted+1
            score.save()
    return JsonResponse(score.serialize(), safe=False)

@csrf_exempt
def newscore(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        group = Group.objects.get(pk=int(data.get("groupid")))
        score = Scores(group=group, user=request.user)
        score.save()
    return JsonResponse(score.serialize(), safe=False)

@csrf_exempt
def delete(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        groupid=int(data.get("groupid"))
    if Group.objects.filter(pk=groupid).exists():
        Group.objects.get(pk=groupid).delete()
    groups = Group.objects.all()
    return JsonResponse([group.serialize() for group in groups], safe=False)


def profile(request, username):
    scores = Scores.objects.filter(user=User.objects.get(username=username)).all()
    return render(request, 'trivia/profile.html', {
        "scores" : scores,
        "profile" : username
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
