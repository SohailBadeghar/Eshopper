from django import forms
from .models import *

'''
This is Django Signup Form and there validations and error will be set here custom validations.
'''
class SignupForm(forms.ModelForm):
    class Meta:
        model= CustomUserModel
        fields=('first_name','last_name','email','password')
        labels ={'first_name':'','last_name':'','email':'','password':''}
        error_messages = {
            'first_name':{'required':'Please enter a first_name'},
            'last_name':{'required':'Please enter a last_name'},
            'email':{'required':'Please enter a email address'},
            'password':{'required':'Please enter a valid password'}, }
            
        widgets = {
                'password':forms.PasswordInput(attrs={'class':'myclass','placeholder':'Password'}),
                'first_name':forms.TextInput(attrs={'class':'myclass','placeholder':'First_name '}),
                'last_name':forms.TextInput(attrs={'class':'myclass','placeholder':'Last_name '}),
                'email':forms.TextInput(attrs={'class':'myclass','placeholder':'Email Address '}),}
        
        

'''
This is the userProfile Form Which is used to get the information About the user.
'''       
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=('mobile_number','country','state','city','address_1','address_2','zipcode')
        widgets = {
            'mobile_number':forms.NumberInput(attrs={'class':'form-control col-md-12', 'placeholder':'enter phone number'}),
            'country':forms.TextInput(attrs={'class':'form-control col-md-12', 'placeholder':'enter phone number'}),
            'state':forms.TextInput(attrs={'class':'form-control col-md-12', 'placeholder':'enter phone number'}),
            'city':forms.TextInput(attrs={'class':'form-control col-md-12','placeholder':'Please Enter  city'}),
            'address_1':forms.TextInput(attrs={'class':'form-control col-md-12','placeholder':'Please Enter  address_1'}),
            'address_2':forms.TextInput(attrs={'class':'form-control col-md-12','placeholder':'Please Enter  address_2'}),
            'zipcode':forms.TextInput(attrs={'class':'form-control col-md-12','placeholder':'Please Enter  zipcode'}),
        }

        
'''
This is the Contactus From For the query Any update requiure for that purpose this form is created.
'''
class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields=('name','email','contact_no','subject','message')
        labels = {'name':'Full Name :','email':'Email Address:','contact_no':'Contact Number','subject':'Subject :','message':'Message :'}
        error_messages = {
            'name':{'required':'Please Enter a Full Name'},
            'email':{'required':'Email Address Required'},
            'contact_no':{'required':'Mobile Number Required'},
            'city':{'required':'Please Enter a City'},
            'subject':{'required':'Please Enter a Subject'},
            'message':{'required':'Please Enter a Message'},
        }
        widgets = {
            'name':forms.TextInput(attrs={'class':'myclass','placeholder':'Full Name'}),
            'email':forms.TextInput(attrs={'class':'myclass','placeholder':'Email Address'}),
            'contact_no':forms.TextInput(attrs={'class':'myclass','placeholder':'Mobile Number'}),
            'city':forms.TextInput(attrs={'class':'myclass','placeholder':'City'}),
            'subject':forms.TextInput(attrs={'class':'myclass','placeholder':'Subject'}),
            'message':forms.Textarea(attrs={'cols': 40, 'rows': 8}),


        }
