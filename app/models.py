from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta    
import hashlib


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=24)
    
    def __str__(self):
        return self.username
    
GENDER_CHOICES = (
    (None, 'select your gender'),
    ('male', "male"),
    ('female', "female"),
    ) 

LANGUAGE_CHOICES = (
    ('language1','language1'), ('language2','language2'), ('language3','language3'), ('language4','language4'),
    ('language5','language5'), ('language6','language6'), ('language7','language7'), ('language8','language8'),
    ('language9','language9'), ('language10','language10'),
    )
OCCUPATION_CHOICES = (
    ('Teacher','Teacher'), ('Businessman','Businessman'), ('Lawyers','Lawyers'), ('Defence','Defence'),
    ('IAS','IAS'), ('Govt Services','Govt.Services'), ('Doctors','Doctors'), ('occu8','occup8'),
    ('occupation9','occupation9'), ('occupation10','occupation10'),
    )	
RELIGION_CHOICES = (
    ('Hindu','Hindu'), ('Christian','Christian'), ('Sikh','Sikh'), ('Jain','Jain'),
    ('Buddhist','Buddhist'), ('Muslim','Muslim'), ('religion7','religion7'), ('religion8','religion8'),
    ('religion9','religion9'), ('religion10','religion10'),
    )      
CASTE_CHOICES = (
    ('caste1','caste1'), ('caste2','caste2'), ('caste3','caste3'), ('caste4', 'caste4'),
    ('caste5','caste5'), ('caste6','caste6'), ('caste7','caste7'), ('caste8','caste8'),
    ('caste9','caste9'), ('caste10','caste10'),
    )   
CITY_CHOICES = (
    ('city1','city1'), ('city2','city2'), ('city3','city3'), ('city4','city4'),
    ('city5','city5'), ('city6','city6'), ('city7','city7'), ('city8','city8'),
    ('city9','city9'), ('city10','city10'),
    )   
STATE_CHOICES = (
    ('state1','state1'), ('state2','state2'), ('state3','state3'), ('state4','state4'),
    ('state5','state5'), ('state6','state6'), ('state7','state7'), ('state8','state8'),
    ('state9','state9'), ('state10','state10'),
    )   
COUNTRY_CHOICES = (
    ('country1','country1'), ('country2','country2'), ('country3','country3'), ('country4','country4'),
    ('country5','country5'), ('country6','country6'), ('country7','country7'), ('country8','country8'),
    ('country9','country9'), ('country10','country10'),
    )   

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)
    birth_date = models.DateField(null=True, blank=True) 
    height = models.CharField(max_length=24, blank=True, null=True, default='')  
    bio = models.TextField(max_length=500, blank=True)  
    image = models.ImageField(default='default.jpg', upload_to = 'images')  
    qualification = models.CharField(max_length=24, null=True, default='')
    occupation = models.CharField(choices=OCCUPATION_CHOICES, max_length=50, default='')
    salary = models.IntegerField(null=True, default=0)

    religion = models.CharField(choices=RELIGION_CHOICES, max_length=24, default='')  
    caste = models.CharField(choices=CASTE_CHOICES, max_length=50, default='')  
    language = models.CharField(choices=LANGUAGE_CHOICES, max_length=50, default='')   
    
    # city = models.CharField(max_length=30, blank=True)
    city =  models.CharField(choices=CITY_CHOICES, max_length=50, default='')
    state =  models.CharField(choices=STATE_CHOICES, max_length=50, default='')
    country =  models.CharField(choices=COUNTRY_CHOICES,max_length=50, default='')    
      
 
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)        
    post_save.connect(create_user_profile, sender=CustomUser)

    def __str__(self):
        if not self.user:
            return "Anonymous"
        return self.user.username

    # Override the save method of the model
    def save(self, **kwargs):
        super().save()


    #@property
    def age_calc(self):
        now = datetime.now().date()
        self.age = (now - self.birth_date).days // 365
        # return age


def calculate_hash(file):  # Calculate hash value of uploaded image file.
    hasher = hashlib.md5()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()

class Addimg(models.Model):    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="propics")
    propic = models.ImageField(upload_to="images") 
    propic_hash = models.CharField(max_length=10,default='', blank=True, null=True, unique=True)
   
    def __str__(self):
        return self.propic.name

    def save(self, *args, **kwargs):
        # Calculate hash value of the uploaded image
        new_hash = calculate_hash(self.propic.file)

        # Check if a profile picture with the same hash exists
        if Addimg.objects.filter(propic_hash=new_hash).exists():
            # Handle duplicate image
            # For example, reject the upload or link to the existing profile
            pass
        else:
            # Save the profile picture and its hash value
            self.propic_hash = new_hash
            super().save(*args, **kwargs)
            