from django import forms
from .models import *


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields= [
                'payment_gateway','name','mobile','email','billing_address_1','billing_address_2',
                'billing_state','billing_city','billing_zipcode','shipping_address_1',
                'shipping_address_2','shipping_city','shipping_state','shipping_zipcode'
                ]
