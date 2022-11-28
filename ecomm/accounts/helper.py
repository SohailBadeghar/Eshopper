from ecomm.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
import uuid
from django.template.loader import render_to_string





def send_forget_password_email(email,email_token,*args):
   
    subject = 'Your foreget password link '
    recipient_list = [email]
    email_from = EMAIL_HOST_USER   
    messages = f'Hi, click on this link to reset your password http://127.0.0.1:8000/accounts/change_password/{email_token}/'
    Msg = EmailMultiAlternatives(subject,messages,email_from,recipient_list)
    Msg.send()
    return True 



def send_account_activation_email(email,messages,*args):
   
    subject = 'Activate your eshoper account'
    recipient_list = [email]
    email_from = EMAIL_HOST_USER    
    Msg = EmailMultiAlternatives(subject,messages,email_from,recipient_list)
    Msg.send()
    return True


# def send_account_activation_email(eamil,):
#     html_body = render_to_string("products/orderplaced_temp.html", )

#     message = EmailMultiAlternatives(
#         subject = 'Activate your eshoper account'
#         body="To verify Your Mail Of Eshopper",
#         from_email='sohailbadeghar561@gmail.com',
#         to=[email]
#         )
#     message.attach_alternative(html_body, "text/html")
#     message.send(fail_silently=False)