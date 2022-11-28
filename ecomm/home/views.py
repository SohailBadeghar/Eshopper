from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponseRedirect
from products.models import *
from django.template.defaulttags import register
from django.views.generic import ListView, DetailView, View
from django.views.generic.base import TemplateView,RedirectView


'''
This function is responsible for showing all the catogories , banner deatils ,all products on index or home page.
'''
class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            'cats' : Category.objects.filter(parent = None),
            'banners' :  BannerSlider.objects.all(),
            'products' : Product.objects.all()
        }
        return context
    

'''
This Function is responsible for showing  all the shop details of product.
'''
class HomeView(ListView):
    model = Product
    paginate_by = 3
    template_name = "accounts/product_list.html"   

    def get_context_data(self,**kwargs):
        context = super(HomeView,self).get_context_data(**kwargs)
        context['cats'] = Category.objects.filter(parent=None)
        return context

@register.filter
def get_range(value):
    return range(value)

    