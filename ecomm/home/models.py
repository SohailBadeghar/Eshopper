from django.db import models
from django.db.models.signals import pre_save
from django.dispatch  import receiver
from django.template.defaultfilters import slugify


DISCOUNT_DEALS = (
    ('HOT DEALS', 'HOT DEALS'),
    ('New Arrivals','New Arrivals'),)

class BannerSlider(models.Model):
    Image = models.ImageField(upload_to="product")
    Discount_Deals = models.CharField(choices=DISCOUNT_DEALS, max_length =255)
    slug = models.SlugField(max_length=200 , null=True ,blank=True)
    Title = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Price_tag_Image = models.ImageField(upload_to="product", null=True, blank=True)

    def __str__(self):
        return self.Title
    
    
'''
Pre_save signal written for the Banner Slider in Slugify Feild.
'''
@receiver(pre_save, sender=BannerSlider)
def task_handelr(sender,instance,**kwargs):
    print("You Printed me")
    print(slugify(instance.Title))
    instance.slug = (slugify(instance.Title))

