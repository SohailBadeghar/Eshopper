from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import AbstractUser
from .manager import Usermanager
from django.db.models.signals import post_save
from django.dispatch import receiver
from .helper import send_account_activation_email
import uuid
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now= True)
    created_by = models.CharField(max_length=255, default='dj')
    updated_at = models.DateTimeField(auto_now_add= True)
    updated_by = models.CharField(max_length=255, default='dj')

    class Meta:
        abstract = True

CHOICES =(
    ("N", "Normal"),
    ("F", "Fcaebook"),
    ("G", "Google"),
    ("T", "Twitter"),
)   

class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    token_no = models.CharField(max_length=255 )
    status = models.BooleanField(default=False)
    fb_token = models.CharField(max_length=100,null=True,blank=True,default=None)
    own_token = models.CharField(max_length=200,null=True,blank=True,default=None)
    twitter_token =  models.CharField(max_length=100,null=True,blank=True,default=None)
    google_token = models.CharField(max_length=100,null=True,blank=True,default=None)
    registration_method =  models.CharField(max_length=1,  choices = CHOICES, default='N')

    object = Usermanager()

    def __str__(self):
        return self.email
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),
("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),
("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),
("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),
("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),
("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),
("Puducherry","Puducherry"))

class UserProfile(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="CustomUserModel")
    image = models.ImageField(default="",upload_to='profile_pics')
    mobile_number = models.CharField(max_length=12,null=True, blank=True )
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES,max_length=50)
    country = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    default = models.BooleanField(_("Default"), default=False)

    def __str__(self):
        return (self.user.first_name)

class ContactUs(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=12)
    message = models.TextField()
    note_admin = models.TextField(max_length=100 , blank=True, null=True)


    def __str__(self):
        return self.name
    

'''
This function is written for post_save signals for the Email verification.After user signup this will work.
'''
@receiver(post_save , sender = CustomUserModel)
def  send_email_token(sender , instance , created , **kwargs):
    try:
        if created:
            email = instance.email
            email_token = str(uuid.uuid4())
            instance.token_no = email_token
            instance.save()
            messages = f'Hi, click on this link to verify your account http://127.0.0.1:8000/accounts/activate_email/{email_token}/'
            send_account_activation_email(email,messages)
    except Exception as e:
        print(e)