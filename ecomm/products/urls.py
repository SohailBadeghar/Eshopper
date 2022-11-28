from django.urls import path
from django.conf import settings
from .views import *

urlpatterns = [
    path('product_details/<int:pk>/',ProductDetailsView.as_view(), name = 'product_details'),
    path('productfilter/<str:id>',ProductFilterView.as_view(),name='productfilter'),
    path('searchproduct/',searchproduct.as_view(),name='searchproduct'),
    path('search_product/', ProfileSearchView.as_view(), name="search_product"),

    path('add_to_cart/<int:id>',AddToCartView.as_view(),name='add_to_cart'),
    path('remove_cart_item/<str:pk>/',RemoveCartItemView.as_view(),name='remove_cart_item'),
    path('minuscart/', minus_cart.as_view(),name='minuscart'),
    path('removecart/', remove_cart.as_view(),name='removecart'),
    path('cart/',CartView.as_view(),name='cart'),
    
    path('addwishlist/<int:id>/',addwishlist,name='addwishlist'),
    path('removewishlist/<int:id>/',removewishlist.as_view(),name='removewishlist'),
    path('showwishlist/',showwishlist,name='showwishlist'),

    path('address/', address, name="address"),

    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name="create-checkout-session"),
    path('PaymentDone/', PaymentDone, name="PaymentDone"),
    path('checkouts', create_checkout, name="checkouts"),
    path('pay', pay, name="pay_cancel"),

    path('place_order/',CheckOutView.as_view(),name='place_order'),
    path('Tracking_Order/', Tracking_Order.as_view(),name='Tracking_Order'),
    path('Order_History', Order_History.as_view(), name="Order_History"),

    path('success/', pay_success.as_view(), name="pay_success"),
    path('complete/', paymentcomplete, name="complete"),
    path('cancel', pay_cancel.as_view(), name="pay_cancel"),
    path('success/',success,name='success'),

]



