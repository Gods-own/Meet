from django.test import Client, TestCase
from .models import User, Countries, Interests, Message, Activities, Events, Room, Liked
from django.core.files.uploadedfile import SimpleUploadedFile
from pathlib import Path
import os

# Create your tests here.

class MeetTestCase(TestCase):
    def setUp(self):
        
        # Create user model
        a1 = User.objects.create(username="Mary", email="sanders@gmail.com", password="good", age=20, dateofbirth="2001-11-23", gender="Female")
        # a1.age = 20
        # a1.dateofbirth = "2001-11-23"
        # a1.gender = "Female"
        a2 = User.objects.create(username="Gogo", email="foo@gmail.com", password="badss", age=25, dateofbirth="1995-12-12", gender="Male")
        # a2.age = 25
        # a2.dateofbirth = "1995-12-12"
        # a2.gender = "Male"
        a3 = User.objects.create(username="Victor", email="boy@gmail.com", password="wonderful", age=23, dateofbirth="1998-05-12", gender="Male")
        # a3.age = 23
        # a3.dateofbirth = "1998-05-12"
        # a3.gender = "Male"


        # Create interest model
        b1 = Interests.objects.create(hobbies="Gardening")
        b1.user_hobby.add(a1)
        b2 = Interests.objects.create(hobbies="Painting")
        b2.user_hobby.add(a1)
        b3 = Interests.objects.create(hobbies="Drawing")
        b3.user_hobby.add(a2)
        b4 = Interests.objects.create(hobbies="Movies")
        b4.user_hobby.add(a2)
        b5 = Interests.objects.create(hobbies="Cooking")
        b5.user_hobby.add(a2)
        b6 = Interests.objects.create(hobbies="Dancing")
        b6.user_hobby.add(a3)

        # Create Country model
        d1 = Countries.objects.create(country="Angola")
        d1.user_country.add(a1)
        d2 = Countries.objects.create(country="Algeria")
        d2.user_country.add(a2)
        d3 = Countries.objects.create(country="Nigeria")
        d3.user_country.add(a3)

        # Create Activity model
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        media = os.path.join(BASE_DIR, 'meet\static\meet\pink-dress.jpg')
        image = SimpleUploadedFile(name='pink-dress.jpg', content=open(media, 'rb').read(), content_type='image/jpeg')
        e1 = Activities.objects.create(poster=a3, activity="hello everyone, how are you all doing", picture=image, hobby=b6)
        e2 = Activities.objects.create(poster=a1, activity="not gonna lie, how are you all doing", picture=image, hobby=b2)
        e3 = Activities.objects.create(poster=a3, activity="that's nice", picture=image, hobby=b1)
        e4 = Activities.objects.create(poster=a2, activity="are you good to go", picture=image, hobby=b4)

        # Create Room model
        c1 = Room.objects.create(room="MG12754", user1=a1, user2=a2)
        c2 = Room.objects.create(room="GM21794", user1=a2, user2=a1)
        c2 = Room.objects.create(room="MV13034", user1=a1, user2=a3)

    def test_citizen_count(self):
        a = User.objects.get(username="Mary")
        b = User.objects.get(username="Victor")
        self.assertEqual(a.citizen.count(), 1)
        self.assertEqual(a.citizen.count(), 2)

    def test_citizen_count(self):
        a = User.objects.get(username="Mary")
        b = User.objects.get(username="Gogo")
        self.assertEqual(a.hobbysist.count(), 2)
        self.assertEqual(b.hobbysist.count(), 3)

    def test_is_valid_likes(self):
        a = Activities.objects.get(pk=1)
        a.likes = -1
        a.save()
        self.assertFalse(a.is_valid_likes())


         # Create Liked model
        # f1 = Liked.objects.create(room="MG12754", user1=a1, user2=a2)
        # f2 = Liked.objects.create(room="GM21794", user1=a2, user2=a1)
        # f2 = Liked.objects.create(room="MV13034", user1=a1, user2=a3)
