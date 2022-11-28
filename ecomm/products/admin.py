from django.contrib import admin
from .models import *
from mptt.admin import DraggableMPTTAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','short_description','price','special_price','quantity','category' )


class CategorytAdmin(admin.ModelAdmin):
    list_display = ('name','slug' )


class orderdetailAdmin(admin.ModelAdmin):
    list_display = ('order','product','status','amount')


admin.site.register(Product,ProductAdmin)
admin.site.register(Category,DraggableMPTTAdmin)
admin.site.register(Product_Attributes)
admin.site.register(Product_Attributes_Values)
admin.site.register(Product_Attributes_Details)
admin.site.register(Coupon)
admin.site.register(CustomerOrder)
admin.site.register(WishList)
admin.site.register(PaymentGateway)
admin.site.register(Cart)
admin.site.register(ProductImages)
admin.site.register(OrderDetails,orderdetailAdmin)













# Register your models here.
