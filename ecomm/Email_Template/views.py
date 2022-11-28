from django.shortcuts import render
from ecomm.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives



def send_mails(request,*args):
    # if request.method == 'POST':
    #         email = request.POST.get('email')
    #         subject = request.POST.get('subject')
    #         content = request.POST.get('content')
    #         Template = request.POST.get('html')

    Msg = EmailMultiAlternatives(args[0], args[1], EMAIL_HOST_USER, [args[3]])
    Msg.attach_alternative(args[2],"text/html")
    Msg.send()
    return True
