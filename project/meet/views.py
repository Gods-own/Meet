from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django_countries import countries
from django.db import IntegrityError, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Countries, Interests, Message, Activities, Events, Room, Liked, Notifications
import datetime
from .util import user_age
from django.db.models import Q, F
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# hobbies = ['Reading', 'Collecting', 'Music', 'Sports', 'Travelling', 'Volunteer Work', 'Painting', 'Housework', 'Movies', 
# 'Gospel Music', 'Socializing', 'Photography', 'Scrapbooking', 'Gardening', 'Video Games', 'Fishing', 'Shopping', 'Writing', 
# 'Dancing', 'Cooking', 'Interior Designing', 'Church Activities', 'Christianity', 'Drawing', 'Knitting', 'Fashion', 'Baking', 
# 'Camping', 'Pottery', 'K-drama', 'K-pop', 'Handcraft', 'Designing', 'Astronomy', 'Calligraphy', 'Board Game', 'Coding', 
# 'Language Learning', 'Mixology']

# hobbies.sort()

hobbies = {'Reading':'https://f.hubspotusercontent30.net/hubfs/5191137/blog/Blog-10-essential-reads-to-improve-reading-comprehension.jpg', 
'Music':'https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/YT_Music.jpg', 
'Sports':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTI1fZ6SlO7pKo8MfWfniskSb5DXHmD7bsHKw&usqp=CAU', 
'Travelling':'https://thumbs.dreamstime.com/b/passport-flight-fly-travelling-travel-citizenship-concept-airplane-traveller-air-stock-image-86057681.jpg', 
'Painting':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQtk-VLE8iCEvqguV96IwvtFa9IiGD8TKq3Zw&usqp=CAU', 
'Movies':'https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/101631641/original/417f783ed60d8acbaf9eda4b51494627abb0255e/recomend-you-movies-in-genre-u-want.jpg', 
'Photography':'https://www.adorama.com/alc/wp-content/uploads/2017/06/2-shutterstock_172791128.jpg', 
'Writing':'https://sweetlovemessages.com/wp-content/uploads/2021/02/How-to-Make-Writing-Your-Favorite-Hobby.jpg', 
'Dancing':'https://bath.co.uk/wp-content/uploads/2011/05/fitness-dance.jpg', 
'Cooking':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSnxfZuOo-vTGRPDh5JgYmG78kIYAx4OMAIHg&usqp=CAU', 
'Christianity':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIvftzi9-_kM2ugb5wlzz0qI_s1WjZbrGJwg&usqp=CAU', 
'Knitting':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRTFSG2mQ07l_DhBeydX19vCaISA9qPNo76Pw&usqp=CAU', 
'Fashion':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1Pj5ep4oDYP-lutEp6r1zR3ExYeKhzPh6Aw&usqp=CAU', 
'Pottery':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuuyj_WLlhMvS5AjxCwVBAiciDsR3OwBUntw&usqp=CAU', 
'Coding':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHH4LCiIDn-OGwk8lPD60LVUYGhuFKxmGKOQ&usqp=CAU', 
'Mixology':'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS6G78S2q5MfNuanQ4h8bt6uzPgWR6RTRxjxQ&usqp=CAU'}

# hobbies = sorted(hobbies)


def index(request): 
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        interests = Interests.objects.filter(user_hobby=user)
        user_hobbies = []
        username = User.objects.get(username=request.user)
        no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
        profile = User.objects.get(username=request.user)
        for interest in interests:
            user_hobby = interest.id
            user_hobbies.append(user_hobby)
        users_activities = Activities.objects.filter(hobby__in=user_hobbies)
        # paginator = Paginator(users_activities, 4)
        # page_number = request.GET.get('page')
        # try:
        #     page_obj = paginator.get_page(page_number)
        # except PageNotAnInteger:
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     page_obj = paginator.page(paginator.num_pages)
        return render(request, "meet/index.html", {
            'activities' : users_activities,
            'no_of_notifications': no_of_notifications,
            'profile': profile
        })
    else:
        return HttpResponseRedirect(reverse("login"))

def messages(request):
    user = User.objects.get(username=request.user)
    rooms = Room.objects.order_by("-date_updated").filter(Q(user1=user) | Q(user2=user))
    dms = []
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    profile = User.objects.get(username=request.user)
    for room in rooms.iterator():
        messages = Message.objects.filter(room=room).last()
        dms.append({"content": messages.content, "date_added": messages.date_added.strftime("%b %d %Y")})
    room_dms = zip(rooms, dms)    
    return render(request, "meet/messages.html", {
        "rooms" : rooms,
        "dms" : dms,
        "room_dms" : room_dms,
        "no_of_notifications": no_of_notifications,
        'profile' : profile
    })    

def room(request, userid2, room_name):
    user1 = User.objects.get(username=request.user)
    user2 = User.objects.get(pk=userid2)
    # username = request.GET.get('username', 'Anonymous')
    username = user1.username
    userid1 = user1.id
    usernam = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=usernam).count()  
    print(no_of_notifications)   
    profile = User.objects.get(username=request.user)
    result1 = Room.objects.filter(Q(user1=user1) & Q(user2=user2)).exists()
    result2 = Room.objects.filter(Q(user1=user2) & Q(user2=user1)).exists()
    if result1 == False and result2 == False:
        room = Room.objects.create(room=room_name, user1=user1, user2=user2)
        messages = Message.objects.filter(room=room)[0:25]
        return render(request, 'meet/room.html', {
        'room_name': room_name, 
        'username': username,
        'messages': messages,
        'userid1': userid1,
        'userid2': userid2,
        'user2': user2,
        'no_of_notifications': no_of_notifications,
        'profile': profile
    })
    else:
        room = Room.objects.get(Q(user1=user1) & Q(user2=user2) | Q(user1=user2) & Q(user2=user1))
        messages = Message.objects.filter(room=room)[0:25]

        return render(request, 'meet/room.html', {
            'room_name': room_name, 
            'username': username,
            'messages': messages,
            'userid1': userid1,
            'userid2': userid2,
            'user2': user2,
            'no_of_notifications': no_of_notifications,
            'profile': profile
        })

def create_activity(request):
    user = User.objects.get(username=request.user)
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        activity_image = request.FILES.get("file", None)
        activity_caption = request.POST.get("caption", None)
        activity_hobby = request.POST.get("hobbies", None)
        hobby = Interests.objects.get(hobbies=activity_hobby)
        Activities.objects.create(poster=user, activity=activity_caption, picture=activity_image, hobby=hobby)
        return HttpResponseRedirect(reverse("index"))
    else:
        interests = Interests.objects.filter(user_hobby=user)
        return render(request, 'meet/createActivity.html', {
            'interests' : interests,
            'no_of_notifications': no_of_notifications,
            'profile': profile
        })

# def edit_activity(request, activity_id):
#     activity = Activities.objects.get(pk=activity_id)
#     if request.method == 'POST':
#         activity_caption = request.POST.get("caption", None)
#         activity.activity = activity_caption
#         activity.save()
#         return HttpResponseRedirect(reverse("index"))
#     else:    
#         return render(request, 'meet/editActivity.html', {
#             'activity' : activity
#         })

@csrf_exempt
@login_required
def edit_activity(request, activity_id):
    activity = Activities.objects.get(pk=activity_id)
    try:
       activity = Activities.objects.get(pk=activity_id)
    except Activities.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(activity.serialize())    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        if data.get("activity_caption") is not None:
            activity.activity = data["activity_caption"]
        activity.save()
        return JsonResponse({"message": "Done."}, status=200)
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


def view_post(request, activity_id):
    try:
        activity = Activities.objects.get(pk=activity_id)
    except Activities.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    activity = Activities.objects.get(pk=activity_id)
    return JsonResponse(activity.serialize(), status=200)
    # return render(request, 'meet/viewPost.html', {
    #     'activity' : activity
    # })

def create_event(request):
    user = User.objects.get(username=request.user)
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    profile = User.objects.get(username=request.user)
    if request.method == 'POST':
        event_title = request.POST.get("title", None)
        event_venue = request.POST.get("venue", None)
        event_description = request.POST.get("description", None)
        event_hobby = request.POST.get("hobbies", None)
        event_country = request.POST.get("location", None)
        event_date = request.POST.get("date", None)
        event_time = request.POST.get("time", None)
        event_date_list = event_date.split("-")
        event_time_list = event_time.split(":")
        print(event_time_list)
        hobby = Interests.objects.get(hobbies=event_hobby)
        country = Countries.objects.get(country=event_country)
        date_of_event = datetime.date(int(event_date_list[0]), int(event_date_list[1]), int(event_date_list[2]))
        time_of_event = datetime.time(int(event_time_list[0]), int(event_time_list[1]))
        Events.objects.create(name=event_title, venue=event_venue, created_by=user, description=event_description, hobby_events=hobby, event_location=country, event_date=date_of_event, event_time=time_of_event)
        return HttpResponseRedirect(reverse("event"))
    else:
        interests = Interests.objects.filter(user_hobby=user)
        countries = Countries.objects.filter(user_country=user)
        return render(request, 'meet/addEvent.html', {
            'interests' : interests,
            'countries' : countries,
            'no_of_notifications': no_of_notifications,
            'profile': profile
        })

def event(request):
    events = Events.objects.all()
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    profile = User.objects.get(username=request.user)
    return render(request, 'meet/event.html', {
        'events' : events,
        'no_of_notifications': no_of_notifications,
        'profile': profile
    })  

def profile(request, user_id):
    if request.user.is_authenticated:
        user = User.objects.get(pk=user_id)
        user2 = User.objects.get(username=request.user)
        activities = Activities.objects.filter(poster=user)
        # paginator = Paginator(activities, 2)
        # page_number = request.GET.get('page')
        interests = Interests.objects.filter(user_hobby=user)
        username = User.objects.get(username=request.user)
        no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count() 
        profile = User.objects.get(username=request.user)
        result1 = Room.objects.filter(Q(user1=user2) & Q(user2=user)).exists()
        result2 = Room.objects.filter(Q(user1=user) & Q(user2=user2)).exists()
        # try:
        #     page_obj = paginator.get_page(page_number)
        # except PageNotAnInteger:
        #     page_obj = paginator.page(1)
        # except EmptyPage:
        #     page_obj = paginator.page(paginator.num_pages)
        if result1 == False and result2 == False:
            room = "generate"
            return render(request, "meet/profile.html", {
                "activities": activities,
                "person": user, 
                "user2": user2,
                "roomName": room,
                "interests": interests,
                'no_of_notifications': no_of_notifications,
                "profile": profile
            })
        else:
            roomquery = Room.objects.get(Q(user1=user2) & Q(user2=user) | Q(user1=user) & Q(user2=user2))
            room = roomquery.room
            return render(request, "meet/profile.html", {
            "activities": activities,
            "person": user, 
            "user2": user2,
            "roomName": room,
            "interests": interests,
            'no_of_notifications': no_of_notifications,
            "profile": profile
            })
    else:
        return HttpResponseRedirect(reverse("login"))

def search(request):
    value = request.GET.get('q', None)
    searcher = User.objects.get(username=request.user)
    interests = Interests.objects.filter(user_hobby=searcher)
    user_hobbies = []
    profile = User.objects.get(username=request.user)
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    for interest in interests:
        user_hobby = interest.id
        user_hobbies.append(user_hobby)
    if value == None or len(value.strip()) == 0:
        return render(request, "meet/search.html", {
            "check": "none",
            "profile": profile,
            "no_of_notifications": no_of_notifications
        })
    else:
        name_search = []
        captalizedValue = value.capitalize()
        if 'country' in request.GET:
            agerange = request.GET.get('age', "")
            gender = request.GET.get('gender', "")
            result = Countries.objects.filter(country__iexact=captalizedValue).exists()
            countries = Countries.objects.all()
            if result == True:
                country_id = Countries.objects.get(country__iexact=captalizedValue)
                # location = country_id.user_country
                # print(country_id.user_country)
                if len(agerange) == 0 and len(gender) == 0:
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies)).exists():
                        get_user = User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies)).distinct()
                        location = get_user
                        return render(request, "meet/search.html", {
                            "results": [{"person": location}],
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                        print('female')
                        print(agerange)
                elif len(agerange) == 0 or agerange == None:
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                        get_user = User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                        location = get_user
                        return render(request, "meet/search.html", {
                            "results": [{"person": location}],
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                elif len(gender) == 0 or gender == None:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                        get_user = User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                        location = get_user
                        return render(request, "meet/search.html", {
                            "results": [{"person": location}],
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                else:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                        get_user = User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                        location = get_user
                        return render(request, "meet/search.html", {
                            "results": [{"person": location}],
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })   
                # return render(request, "meet/search.html", {
                #     "check": "nothing"
                # })        
                # if exists.exists():
                #     location = get_user
                #     print(location)
                #     return render(request, "meet/search.html", {
                #         "results": [{"person": location}]
                #     })
            else:
                for country in countries.iterator():
                    if value.lower() in country.country.lower(): 
                    
                        if len(agerange) == 0 and len(gender) == 0:
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies)).exists():
                                get_user = User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                                print('female')
                                print(agerange)
                        elif len(agerange) == 0 or agerange == None:
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                                get_user = User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                        elif len(gender) == 0 or gender == None:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                                get_user = User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                        else:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                                get_user = User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                        
                if len(name_search) == 0:
                    return render(request, "meet/search.html", {
                        "check": "nothing",
                        "profile": profile,
                        "no_of_notifications": no_of_notifications
                    })
                else:
                    return render(request, "meet/search.html", {
                    "results": name_search,
                    "profile": profile,
                    "no_of_notifications": no_of_notifications
                    
                })
        else:
            agerange = request.GET.get('age', "")
            gender = request.GET.get('gender', "")
            result = User.objects.filter(username__iexact=captalizedValue).exists()
            users = User.objects.all()
            if result == True:
                if len(agerange) == 0 and len(gender) == 0:
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies)).distinct()
                        print(user_id)
                        return render(request, "meet/search.html", {
                            "results": user_id,
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                        print('female')
                        print(agerange)
                elif len(agerange) == 0 or agerange == None:
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                        return render(request, "meet/search.html", {
                            "results": user_id,
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                elif len(gender) == 0 or gender == None:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                        return render(request, "meet/search.html", {
                            "results": user_id,
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })
                else:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                        return render(request, "meet/search.html", {
                            "results": user_id,
                            "profile": profile,
                            "no_of_notifications": no_of_notifications
                        })   
                return render(request, "meet/search.html", {
                    "check": "nothing",
                    "profile": profile,
                    "no_of_notifications": no_of_notifications
                })        
            else:
                for user in users.iterator():
                    if value.lower() in user.username.lower(): 
                        if len(agerange) == 0 and len(gender) == 0:
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies)).exists():
                                user_id = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies)).distinct()
                                name_search.append({"id": user.id, "username": user.username, "userImage": user.userImage})
                                print('female')
                                print(agerange)
                        elif len(agerange) == 0 or agerange == None:
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                                user_id = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                                name_search.append({"id": user.id, "username": user.username, "userImage": user.userImage})
                        elif len(gender) == 0 or gender == None:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                                user_id = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                                name_search.append({"id": user.id, "username": user.username, "userImage": user.userImage})
                        else:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                                user_id = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                                name_search.append({"id": user.id, "username": user.username, "userImage": user.userImage})
                if len(name_search) == 0:
                    return render(request, "meet/search.html", {
                        "check": "nothing",
                        "profile": profile,
                        "no_of_notifications": no_of_notifications
                    })
                else:
                    return render(request, "meet/search.html", {
                        "results": name_search,
                        "profile": profile,
                        "no_of_notifications": no_of_notifications
                    })

@csrf_exempt
@login_required
def sidesearch(request):
    value = request.GET.get('q', None)
    searcher = User.objects.get(username=request.user)
    interests = Interests.objects.filter(user_hobby=searcher)
    user_hobbies = []
    for interest in interests:
        user_hobby = interest.id
        user_hobbies.append(user_hobby)
    if value != None:
        captalizedValue = value.capitalize()
        result = User.objects.filter(username=captalizedValue).exists()
        users = User.objects.all()
        name_search = []
        if 'country' in request.GET:
            agerange = request.GET.get('age', "")
            gender = request.GET.get('gender', "")
            result = Countries.objects.filter(country__iexact=captalizedValue).exists()
            countries = Countries.objects.all()
            if result == True:
                country_id = Countries.objects.get(country__iexact=captalizedValue)
                if len(agerange) == 0 and len(gender) == 0:
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies)).exists():
                        get_user = User.objects.get(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies)).distinct()
                        location = get_user
                        return JsonResponse(location.serialize())
                        print('female')
                        print(agerange)
                elif len(agerange) == 0 or agerange == None:
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                        get_user = User.objects.get(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                        location = get_user
                        return JsonResponse(location.serialize())
                elif len(gender) == 0 or gender == None:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                        get_user = User.objects.get(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                        location = get_user
                        return JsonResponse(location.serialize())
                else:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                        get_user = User.objects.get(Q(citizen=country_id) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                        location = get_user
                        return JsonResponse(location.serialize())   
            else:
                for country in countries.iterator():
                    if value.lower() in country.country.lower(): 
                    
                        if len(agerange) == 0 and len(gender) == 0:
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies)).exists():
                                get_user = User.objects.get(Q(citizen=country) & Q(hobbysist__in=user_hobbies)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                                print('female')
                                print(agerange)
                        elif len(agerange) == 0 or agerange == None:
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                                get_user = User.objects.get(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                        elif len(gender) == 0 or gender == None:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                                get_user = User.objects.get(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
                        else:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                                get_user = User.objects.get(Q(citizen=country) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                                location = get_user
                                name_search.append({"id": country.id, "person": location})
        else:
            agerange = request.GET.get('age', "")
            gender = request.GET.get('gender', "")
            result = User.objects.filter(username__iexact=captalizedValue).exists()
            users = User.objects.all()
            if result == True:
                if len(agerange) == 0 and len(gender) == 0:
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies)).distinct()
                        
                        return JsonResponse([user_i.serialize() for user_i in user_id], safe=False)
                elif len(agerange) == 0 or agerange == None:
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()
                        return JsonResponse([user_i.serialize() for user_i in user_id], safe=False)
                elif len(gender) == 0 or gender == None:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct() 
                        return JsonResponse([user_i.serialize() for user_i in user_id], safe=False)
                else:
                    age_list = agerange.split("-")
                    if User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                        user_id = User.objects.filter(Q(username__iexact=captalizedValue) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()
                        return JsonResponse([user_i.serialize() for user_i in user_id], safe=False)   
            else:
                for user in users.iterator():
                    if value.lower() in user.username.lower(): 
                        if len(agerange) == 0 and len(gender) == 0:
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies)).exists():
                                user_result = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies)).distinct()[0]
                                name_search.append({"id": user_result.id, "username": user_result.username, "userImage": user_result.userImage.url})
                                print('female')
                                print(agerange)
                        elif len(agerange) == 0 or agerange == None:
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).exists():
                                user_result = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(gender=gender)).distinct()[0]
                                name_search.append({"id": user_result.id, "username": user_result.username, "userImage": user_result.userImage.url})
                        elif len(gender) == 0 or gender == None:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).exists():
                                user_result = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1])))).distinct()[0]
                                name_search.append({"id": user_result.id, "username": user_result.username, "userImage": user_result.userImage.url})
                        else:
                            age_list = agerange.split("-")
                            if User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).exists():
                                user_result = User.objects.filter(Q(username__iexact=user.username) & Q(hobbysist__in=user_hobbies) & Q(age__range=(int(age_list[0]), int(age_list[1]))) & Q(gender=gender)).distinct()[0]
                                name_search.append({"id": user_result.id, "username": user_result.username, "userImage": user_result.userImage.url})
        if len(name_search) == 0:
            return JsonResponse({"person":"false"})
        else:
            print(name_search)
            return JsonResponse(name_search, safe=False) 


def editProfile(request):
    user = User.objects.get(username=request.user)
    username = User.objects.get(username=request.user)
    no_of_notifications = Notifications.objects.filter(notification_read=False, notification_user=username).count()
    if request.method == 'POST':
        username = request.POST.get('username', None)
        image = request.FILES.get('image', None)
        if username != None:
            user.username = username
            user.save()
        if image != None:
            user.userImage = image
            user.save()
        return HttpResponseRedirect(reverse("person", kwargs={'user_id': user.id }))
    else:
        return render(request, "meet/settings.html", {
        "profile": user,
        "no_of_notifications": no_of_notifications
    })    


@csrf_exempt
@login_required
def like_post(request, activity_id):

    try:
        activity = Activities.objects.get(pk=activity_id)
    except Activities.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(activity.serialize())

    elif request.method == "PUT":
        liked = Liked.objects.filter(liker=request.user, activity=activity).exists()
        activity1 = Activities.objects.filter(pk=activity_id)
        if liked == False:
            Liked.objects.create(liker=request.user, activity=activity, is_liked=True)
            # activity.likes = activity.likes + 1
            # activity.save()
            activity1.update(likes=F('likes') + 1)
            return JsonResponse({"message": "done."}, status=200)
        else:
            checklike = Liked.objects.get(liker=request.user, activity=activity)
            if checklike.is_liked == False:
                checklike.is_liked = True
                checklike.save()
                # activity.likes =  activity.likes + 1
                # activity.save()
                activity1.update(likes=F('likes') + 1)
                return JsonResponse({"message": "done."}, status=200)
            
            else:
                checklike.is_liked = False
                checklike.save()
                # activity.likes =  activity.likes - 1
                # activity.save()
                activity1.update(likes=F('likes') - 1)
                return JsonResponse({"message": "done."}, status=200)

@csrf_exempt
@login_required
def isliked(request, activity_id):
    activity = Activities.objects.get(pk= activity_id)
    # try:
    #     liked = Liked.objects.get(liker=request.user,  activity=activity)
    # except Liked.DoesNotExist:
    #     return JsonResponse({"error": "Post not found."}, status=404)

    if Liked.objects.filter(liker=request.user, activity=activity).exists() == True:
        liked = Liked.objects.get(liker=request.user,  activity=activity)
    
        return JsonResponse({"liked": liked.is_liked}, status=200)
    else:
        return JsonResponse({"liked": False}, status=200)

@csrf_exempt
@login_required
def notification(request, userid2):    

    user1 = User.objects.get(username=request.user)
    user2 = User.objects.get(pk=userid2)
    # username = request.GET.get('username', 'Anonymous')
    username = user1.username
    userid1 = user1.id
    result1 = Room.objects.filter(Q(user1=user1) & Q(user2=user2)).exists()
    result2 = Room.objects.filter(Q(user1=user2) & Q(user2=user1)).exists()
    if result1 == False and result2 == False:
        return JsonResponse({"message": "Room created!"}, status=200)
    else:
        room = Room.objects.get(Q(user1=user1) & Q(user2=user2) | Q(user1=user2) & Q(user2=user1))
        messages = Message.objects.filter(room=room)
        chat_messages = []
        for message in messages:
            chat_message = message.id
            chat_messages.append(chat_message)
        data = json.loads(request.body)
        if data.get("notification_read") is not None:
            notification = Notifications.objects.filter(notification_message__in=chat_messages)
            notification.update(notification_read=data["notification_read"])
            print(notification)
        return JsonResponse({"message": "message read"}, status=200)      

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            username = User.objects.get(username=user)
            interests = Interests.objects.filter(user_hobby=username)
            if interests.exists() == True:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("addInterests", kwargs={'user_id': username.id })) 
        else:
            return render(request, "meet/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "meet/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        dateofbirth = request.POST["dateofbirth"]
        dateofbirth_list = dateofbirth.split("-")
        gender = request.POST["gender"]
        country = request.POST["country"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        userna = User.objects.filter(username__iexact=username).exists()

        #Ensure fields are filled
        if not username:
            return render(request, "meet/register.html", {
                "message": "Please input username."
            })
        if userna == True:
            return render(request, "meet/register.html", {
                "message": "username taken."
            })    
        if not email:
            return render(request, "meet/register.html", {
                "message": "Please input email."
            })
        if not dateofbirth:
            return render(request, "meet/register.html", {
                "message": "Please input dateofbirth."
            })
        if not gender:
            return render(request, "meet/register.html", {
                "message": "Please select gender."
            }) 
        if not password:
            return render(request, "meet/register.html", {
                "message": "Please input password."
            })        

        # Ensure password matches confirmation

        if password != confirmation:
            return render(request, "meet/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            date_of_birth = datetime.date(int(dateofbirth_list[0]), int(dateofbirth_list[1]), int(dateofbirth_list[2]))
            age = user_age(date_of_birth)
            user = User.objects.create_user(username, email, password, age=age, dateofbirth=date_of_birth, gender=gender)
            # user.age = age
            # user.dateofbirth = date_of_birth
            # user.gender = gender
            result = Countries.objects.filter(country=country).exists()
            if result == True:
                get_country = Countries.objects.get(country=country)
                get_country.user_country.add(user)
            else:
                create_country = Countries.objects.create(country=country)
                create_country.user_country.add(user)
            user.save()
        except IntegrityError:
            return render(request, "meet/register.html", {
                "message": "Username already taken."
            })
        # return HttpResponseRedirect(reverse("index"))
        userId = User.objects.get(username=username)
        return HttpResponseRedirect(reverse("addInterests", kwargs={'user_id': userId.id }))
    else:
        return render(request, "meet/register.html", {
            'countries': countries,
        })

def add_interests(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        interests = request.POST.getlist("hobby")
        print(interests)
        if len(interests) <= 0:
            return render(request, "meet/registerInterest.html", {
                'message' : "Please pick at least one interest",
                'hobbies': hobbies,
                'id': user_id,
            })
        if len(interests) > 2:
            return render(request, "meet/registerInterest.html", {
                'message' : "Please pick at most one interest",
                'hobbies': hobbies,
                'id': user_id,
            })    
        for i in interests:
            result = Interests.objects.filter(hobbies=i).exists()
            if result == True:
                get_interests = Interests.objects.get(hobbies=i)
                get_interests.user_hobby.add(user)
            else:
                create_interests = Interests.objects.create(hobbies=i)
                create_interests.user_hobby.add(user)
        return HttpResponseRedirect(reverse("index"))
        
    else:
        print(hobbies)
        return render(request, "meet/registerInterest.html", {
            'hobbies': hobbies,
            'id': user_id,
            'profile': user
        })
