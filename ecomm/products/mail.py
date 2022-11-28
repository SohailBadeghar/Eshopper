from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def order_placed_mail(eamil,payment):
    html_body = render_to_string("products/orderplaced_temp.html", payment)

    message = EmailMultiAlternatives(
        subject='Django HTML Email',
        body="mail testing",
        from_email='sohailbadeghar561@gmail.com',
        to=[eamil]
        )
    message.attach_alternative(html_body, "text/html")
    message.send(fail_silently=False)