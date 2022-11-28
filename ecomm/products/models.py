from email.policy import default
from random import choices
from django.db import models
from base.models import BaseModel
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey
from accounts.models import CustomUserModel
import uuid
import datetime

# Create your models here.

class Category(BaseModel,MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=False)
    parent = TreeForeignKey('self',blank=True, null=True, related_name='child', on_delete=models.CASCADE )

    class Meta:
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories"   

    def __str__(self):                           
        full_path = [self.name]            
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


'''
For Search Model Manger Query Written .
'''
class ProductQueryset(models.QuerySet):
    def search(self,query=None):
      return self.filter(name__icontains=query)

    def ProductFilter(self,id=None):
        return self.filter(category_id=id)

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQueryset(self.model,using=self.db)
    
    def search(self,query=None):
        return self.get_queryset().search(query)
    
    def ProductFilter(self,id=None):
        return self.get_queryset().ProductFilter(id)


class Product(BaseModel):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    long_description = models.TextField(max_length=255)
    price = models.FloatField(max_length=255)
    special_price = models.FloatField(max_length=255)
    special_price_from = models.DateField(auto_now= True)
    special_price_to = models.DateField(auto_now= True)
    status = models.BooleanField(default=False)
    quantity = models.IntegerField()
    meta_title = models.TextField(max_length=100)
    meta_description = models.TextField(max_length=100)
    meta_keywords = models.TextField(max_length=100)
    category = models.ForeignKey('Category',related_name="products",on_delete=models.CASCADE) 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return self.slug

    def __str__(self) -> str:
        return self.name

    objects = ProductManager()

class ProductImages(BaseModel):
    image =  models.ImageField(upload_to="product")
    status = models.BooleanField(default=False)
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")

    class Meta:
        verbose_name_plural = "productimages"   

class Product_Attributes(BaseModel):
    name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product_attributes" 

    def __str__(self) -> str:
        return self.name


class Product_Attributes_Values(BaseModel):
    product_attribute = models.ForeignKey(Product_Attributes , on_delete=models.CASCADE , related_name="product_attributes_values")
    attribute_value = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product_attributes_values" 

    def __str__(self) -> str:
        return self.attribute_value


class Product_Attributes_Details(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_attributes_details")
    product_attribute = models.ForeignKey(Product_Attributes , on_delete=models.CASCADE , related_name="product_attributes_details")
    product_attribute_value = models.ForeignKey(Product_Attributes_Values , on_delete=models.CASCADE , related_name="product_attributes_details")

    class Meta:
        verbose_name_plural = "product_attributes_details" 

    def __str__(self) -> str:
        return self.product.name



class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price  = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=100)
    no_of_uses = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.coupon_code


STATE_CHOICES = (('Maharashtra','Maharashtra'),('Goa','Goa'),
                ('Gujrat','Gujrat'),('Assam','Assam'),('Chhattisgarh','Chhattisgarh'),
                ('Bihar','Bihar'),('Rajasthan','Rajasthan'),('Punjab','Punjab'),('Karnataka','Karnataka'),
                ('Manipur','Manipur'))
CITY_CHOICES =(('Pune','Pune'),('Mumbai','Mumbai'),
                ('Banglore','Banglore'),('Delhi','Dehli'),('AGRA','AGRA'),
                ('Surat','Surat'),('Vadodra','Vadodra'),('Bhopal','Bhopal'))
PAYMENT_CHOICES =(('wallet','wallet'),('card','card'),
                ('netbanking','netbanking'),('emi','emi'),
                ('paypal','paypal'),('cod','cod'))


class PaymentGateway(BaseModel):
    name = models.CharField(max_length=200)
    class Meta:
            verbose_name_plural = "PaymentGateway" 
    def __str__(self) -> str:
            return self.name


class CustomerOrder(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="order")
    shipping_method= models.CharField( max_length=50, default='rail')
    awb_no = models.CharField(max_length = 200, default=uuid.uuid4)
    payment_gateway = models.ForeignKey(PaymentGateway,on_delete=models.CASCADE , related_name="order")
    transaction_id= models.CharField(max_length=100) 
    status = models.BooleanField(default=False)
    grand_total = models.FloatField()
    shipping_charges =  models.FloatField(default=100)
    coupon = models.OneToOneField(Coupon , on_delete=models.CASCADE , related_name="coupon_used",blank=True,null=True  )
    name = models.CharField(max_length=100) 
    mobile = models.CharField(max_length=10) 
    email = models.EmailField(max_length=100) 
    billing_address_1= models.CharField(max_length=1024,blank=False) 
    billing_address_2 = models.CharField(max_length =100,blank=False) 
    billing_state = models.CharField(choices=STATE_CHOICES,max_length=100,blank=False)
    billing_city = models.CharField(choices=CITY_CHOICES,max_length=100,blank=False) 
    billing_zipcode = models.CharField(max_length=100,blank=False) 
    shipping_address_1= models.CharField(max_length=1024,blank=False) 
    shipping_address_2 = models.CharField( max_length =100,blank=False) 
    shipping_city = models.CharField(choices=CITY_CHOICES,max_length=100,blank=False) 
    shipping_state = models.CharField(choices=STATE_CHOICES, max_length =100,blank=False) 
    shipping_zipcode = models.CharField(max_length=100,blank=False) 


ORDER_STATUS = (
    ('Pending','Pending'),
    ('Order confirmed','Order confirmed'),
    ('Processing Order','Processing Order'),
    ('Quality Check','Quality Check'),
    ('Dispatched Item','Dispatched Item'),
    ('Product Delivered','Product Delivered'),
    )
class OrderDetails(BaseModel):
    order = models.ForeignKey(CustomerOrder , on_delete=models.CASCADE , related_name="orderdetails")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="orderdetails")
    quantity = models.IntegerField()
    date = models.DateField(default=datetime.datetime.today)
    status = models.CharField(max_length=100,choices=ORDER_STATUS,default='pending')
    amount = models.FloatField()

class WishList(BaseModel):
    user = models.ForeignKey(CustomUserModel , on_delete=models.CASCADE , related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name="wishlist")


class Cart(BaseModel):
    user =  models.ForeignKey(CustomUserModel, on_delete=models.CASCADE , related_name="cart")
    product =  models.ForeignKey(Product, on_delete=models.CASCADE , related_name="cart",null=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name  





































































































































































































































































































































































































































































































































































































































































































































































































































































































































