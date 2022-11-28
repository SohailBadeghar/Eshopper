from django.shortcuts import render,HttpResponseRedirect,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login ,logout,update_session_auth_hash
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,SetPasswordForm,PasswordChangeForm
from .helper import send_forget_password_email
import uuid
from django.views import View
from django.contrib.auth.decorators import login_required
import json
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,CreateView ,DeleteView,FormView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


'''
This Function will Check whether the User is verified or not.
'''
class activate_email(View):
    def get(self, request,email_token):
        try:
            user = CustomUserModel.objects.get(token_no= email_token)
            user.is_email_verified = True   
            user.save()
           
        except Exception as e:
            return HttpResponse('Invalid Email token')

        return redirect('login')
    

'''
This Function is Wriiten to Sign up for New user.
'''

class SignUpView(CreateView):  
    model = CustomUserModel  
    fields=('first_name','last_name','email','password')
    success_url = '/accounts/login_1/' 

    def form_valid(self,form,commit=True):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        if commit:
            user.save()
        messages.success(self.request,'your account has been signed up successfully!')
        return super().form_valid(form)


'''
This function is Used to User Login and Check whether user is authanticated or not.
'''
class LoginView(View):
    return_url = None

    def get(self, request,*args):
        LoginView.return_url = request.GET.get('return_url')
        form = AuthenticationForm()
        return render(self.request, 'accounts/login.html',{'form':form })

    def post(self,request,*args):
        fm = AuthenticationForm(request = self.request,data=self.request.POST)
        if fm.is_valid():
            umail = fm.cleaned_data.get('username')
            user = CustomUserModel.object.get(email=umail)
            upass = fm.cleaned_data.get('password')

            if not user.is_email_verified:
                messages.warning(request, 'Your account is not verified.')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = authenticate(username=umail,password=upass)
        
            if user is not None or user.is_superuser==True:
                login(self.request, user)
                messages.success(request,f'welcome  {user.first_name} !!!!!!')
                request.session['user'] = user.id

                if LoginView.return_url:
                    return HttpResponseRedirect(LoginView.return_url)
                else:
                    LoginView.return_url = None
                    return redirect('homepage')
            messages.success(request, 'user is not registered ')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:      
            messages.success(self.request,'wrong ')
        return render(self.request, 'accounts/login.html',{'form':fm, 'errors': fm.errors})

    
'''
This function is used to reset the new password using Setpassword form.
'''

class ResetPasswordView(View):

    def get(self,request,token):
        fm = SetPasswordForm(user=request.user)
        return render(request,'accounts/changepassword.html',{'forms':fm})

    def post(self,request,token):
        if request.method == 'POST':
            user_token = CustomUserModel.objects.get(own_token=token)
            if user_token:
                if request.POST.get('new_password1') == request.POST.get('new_password2'):
                    user_token.set_password(request.POST.get('new_password1'))
                    user_token.save()
                    messages.success(request,'Password Change Successfully')
                    return redirect('login')
                else:
                    messages.success(request,'both msg does not match')
                    fm = SetPasswordForm(user=request.user)
                    return render(request,'accounts/changepassword.html',{'forms':fm})

            else:
                messages.success(request,'invalid or expired token for password reset or check ur email')
                return render(request, 'accounts/forgetpassword.html')
            

            
'''
This function is responsible for forget password ,user can change password using mail.
'''
class ForgetPasswordView(View):

    def get(self,request):
        return render(request, 'accounts/forgetpassword.html')

    def post(self,request):
        username = request.POST.get('username')

        if not CustomUserModel.objects.filter(email=username).first():
            messages.success(request,'Not User found with this username.')
            return redirect('Forget_Password')
        
        user_obj = CustomUserModel.objects.get(email=username)
        email_token = str(uuid.uuid4())
        send_forget_password_email(user_obj,email_token)
        user_obj.own_token = email_token
        user_obj.save()
        messages.success(request,' An Email is Sent.')
        return render(request, 'accounts/resetconfg.html')




'''
Change password with old password for user profile function.
'''
class ChangePasswordView(View):

    def get(self,request):
        fm = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/newpassword.html',{'forms':fm})

    def post(self,request):
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user,data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                messages.success(request,'Password Change Successfully')
                return render(request, 'accounts/newpassword.html',{'forms':fm})


'''
Logout View for user logout function.
 '''
class LogoutView(View):
    def get(self, request):
        self.request.session.clear()
        logout(request)
        return HttpResponseRedirect('/')


'''
This view is genric view that is createView  will give us to create Profile .
'''
class UserProfilView(CreateView):  
    model = UserProfile  
    form_class = UserProfileForm
    success_url = '/' 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    
'''
This View is for showing the list of addresss of User.
'''
class AddressView(ListView):
    template_name = 'accounts/userprofile_list.html'
    def get_queryset(self):
        queryset =  UserProfile.objects.filter(user=self.request.user)
        return queryset


'''
This View is for edit the list of addresss of User.
'''
class edit_address(UpdateView):  
    model = UserProfile  
    form_class = UserProfileForm
    success_url = '/' 

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


'''
This View is for delete the list of addresss of User.
'''
class delete_address(DeleteView):
     model = UserProfile  
     success_url = '/'  


'''
This View is for set the default  addresss of User.
'''
class set_default(View):
    def get(self,request,pk):
        UserProfile.objects.filter(user=request.user, default=True).update(default=False)
        UserProfile.objects.filter(id=pk, user=request.user).update(default=True)
        return redirect("/accounts/adresses")  


'''
This View is for taking the contact us form detail from user.
'''
class ContactUs(FormView):
    template_name = 'accounts/contactus.html'
    form_class = ContactUsForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super(ContactUs, self).form_valid(form)
    
    