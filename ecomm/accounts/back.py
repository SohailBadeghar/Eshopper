from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as dj_login,logout,update_session_auth_hash
from .models import *
from .forms import *
from django.contrib import messages as mymessage
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm
from .helper import send_account_activation_email
import uuid


#signup view function

def activate_email(request , id):
    try:
        user = CustomUserModel.objects.get(email_token= id)
        user.is_email_verified = True   
        user.save()
        return redirect('index')
    except Exception as e:
        return HttpResponse('Invalid Email token')


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm =SignupForm(request.POST)
            password = request.POST.get('password')

            if fm.is_valid():
                user =fm.save()
                user.set_password(password)
                user.save()

                messages.success(request,'your account has been signed up successfully!')
                return redirect('login')
        else:
            fm = SignupForm()
        return render(request, 'accounts/Registration.html',{'forms':fm})  

    else:
        return HttpResponseRedirect('/')


#login_page view function

def User_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm = AuthenticationForm(request = request,data=request.POST)

            if fm.is_valid():
                umail = fm.cleaned_data.get('username')
                upass = fm.cleaned_data.get('password')

                # if not umail.is_email_verified:
                #     messages.warning(request, 'Your account is not verified.')
                #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                user = authenticate(username=umail,password=upass)
                if user is not None:
                    dj_login(request, user)
                    mymessage.success(request,f'welcome  {user.first_name} !!!!!!')
                    return HttpResponseRedirect('/')
        else:      
            fm = AuthenticationForm()
        return render(request, 'accounts/login.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')




#Change password without old password for user profile function
# @login_required(login_url='accounts/login/') 
def Change_new_Password(request,token):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = SetPasswordForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Change Successfully')
                # return HttpResponseRedirect('/')
        else:
            fm = SetPasswordForm(user=request.user)
        return render(request,'accounts/ChangePassword.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/login/')
    



#ForgetPassword View Function
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not CustomUserModel.objects.filter(email=username).first():
                messages.success(request,'Not User found with this username.')
                return redirect('/Forget_Password/')
            user_obj = CustomUserModel.objects.get(email=username)
            email_token = str(uuid.uuid4())
            messages = f'Hi, click on this link to reset your password http://127.0.0.1:8000/accounts/change_password/{email_token}/'

            send_account_activation_email(user_obj,messages)
            messages.success(request,' An Email is Sent.')
            return render(request, 'accounts/Reset_conf.html')
    except Exception as e:
         print(e)
    return render(request, 'accounts/ForgetPassword.html')




def reset_template(request):
    return render(request, 'accounts/Reset_conf.html')


# Change password with old password for user profile function

def ChangePassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Change Successfully')
                return render(request, 'accounts/new_pass.html',{'forms':fm})
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/new_pass.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')



#logout View for user logout function

def User_logout(request):
    logout(request)
    return HttpResponseRedirect('/')



# def UserProfiePage(request):
#     if request.method == 'POST':
#         fm =UserProfileForm(request.POST)
#         if fm.is_valid():
#             fm.save()
#             messages.success(request,'Your UserProfile details has been  successfully completed!')
#             # return HttpResponseRedirect('/')
#             return render(request, 'accounts/User_Profile.html',{'forms':fm})
#     else:
#         fm = UserProfileForm()
#     return render(request, 'accounts/User_Profile.html',{'forms':fm})  




def ContactUs(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fm =ContactUsForm(request.POST)
            if fm.is_valid():
                user =fm.save()
                user.save()
                messages.success(request,'Thank You for Submitting Form!')
                return HttpResponseRedirect('/')
        else:
            fm = ContactUsForm()
        return render(request, 'accounts/ContactUs.html',{'forms':fm})
    else:
        return HttpResponseRedirect('/')



def UserProfilePage(request):
    userinfo = CustomUserModel.objects.get(id=request.user.id)
    if request.method == 'POST':
        mobile_number = request.POST['mobile_number']
        add1 = request.POST['address_1']
        add2 = request.POST['address_2']
        city =request.POST['city']
        state = request.POST['state']
        country =request.POST['country']
        zipcode = request.POST['zipcode']
        profile = UserProfile(user =request.user, mobile_number=mobile_number,
                                address_1=add1,address_2=add2,city=city,
                                state=state,country=country,zipcode=zipcode)
        profile.save()
        messages.success(request,'Your UserProfile details has been  successfully completed!')
        return render(request, 'accounts/userprofile.html',{'userinfo':userinfo})

    else:
        # fm = UserProfileForm()
     return render(request, 'accounts/userprofile.html',{'userinfo':userinfo})  



@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = UserProfile.objects.get(pk=id, user=request.user)
        address.mobile_number = request.POST['mobile_number']
        address.address_1 = request.POST['address_1']
        address.address_2 = request.POST['address_2']
        address.city =request.POST['city']
        address.state = request.POST['state']
        address.country =request.POST['country']
        address.zipcode = request.POST['zipcode']
        address.save()
        return redirect("/accounts/adresses")
    else:
        userinfo = CustomUserModel.objects.get(id=request.user.id)
        address = UserProfile.objects.get(pk=id, user=request.user)
        add1 = address.address_1
        add2 = address.address_2
        mob = address.mobile_number
        city = address.city
        state =address.state
        country=address.country
        zipcode = address.zipcode
        context={'id':address.id ,'add1':add1,'add2':add2,'mob':mob,'city':city,'state':state,'country':country,'zipcode':zipcode,'userinfo':userinfo}

        return render(request,"accounts/editaddress.html", context)



@login_required
def delete_address(request, id):
    address = UserProfile.objects.get(pk=id, user=request.user).delete()
    return redirect("/accounts/adresses")  



@login_required
def set_default(request, id):
    UserProfile.objects.filter(user=request.user, default=True).update(default=False)
    UserProfile.objects.filter(pk=id, user=request.user).update(default=True)
    return redirect("/accounts/adresses")   


def adresses(request):
    adresses= UserProfile.objects.filter(user=request.user)
    print(adresses,'2222@@@@@@@@@@@@@@')
    return render(request,'accounts/adresses.html',{'adresses':adresses})


