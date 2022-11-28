# from django.template import RequestContext
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import *
from .templatetags.cart import *
from django.contrib import messages
from .forms import *
from django.db.models import Q
from django.http import JsonResponse
import datetime
import json
from accounts.models import *
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, View
from django.views import View
from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import os
import braintree
import datetime
from products.mail import order_placed_mail
from base.middlewares.auth import auth_middleware
from home.models import BannerSlider

'''
In this Details view Shows the single Product detail on the detailview on clicking on the product.
'''
class ProductDetailsView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.filter(parent=None)
        return context

class ProfileSearchView(View):
    def get(self,request):
        products = Product.objects.filter(name__icontains=self.request.GET.get('search') )
        return render(request, 'home/index.html', {'products':products})


    
class ProductFilterView(View):
    def get(self, request, *args, **kwargs):
        cats = Category.objects.filter(parent=None)
        id = self.kwargs.get('id')
        products = Product.objects.filter(category_id=id)
        banners = BannerSlider.objects.all()
        return render(request, 'home/index.html', {'products':products, 'cats':cats , 'banners':banners})
       


class CartView(View):
    @method_decorator(auth_middleware)
    def get(self,request): 
        carts = ''
        if request.user.is_authenticated:
            user = request.user
            cats = Category.objects.filter(parent = None) 
            total = total_cart_price(carts)
            carts = Cart.objects.filter(user=user)
            if carts:
                return render(request,'products/cart.html',{'cats':cats,'carts':carts,'total':total})
            else:
                return render(request,'products/emptycart.html')
            
    def post(self,request): 
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
        carts = Cart.objects.filter(user=request.user)

        if not coupon_obj.exists():
            messages.warning(request, 'Invalid Coupon')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if total_cart_price(carts) < coupon_obj[0].minimum_amount:
            messages.warning(request, f'amount should be greater than {coupon_obj[0].minimum_amount}')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


        if coupon_obj[0].is_expired:
            messages.warning(request, f'coupon expired')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        total = total_cart_price(carts, coupon_obj[0])
        coupon_obj.update(is_expired = True)
        coupon_obj[0].save()
        messages.success(request, 'Coupon applied')
        return render(request, 'products/cart.html',{'carts':carts,'total':total})


class remove_cart(View):
    def get(self,request):
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        data={}
        return JsonResponse(data)

class minus_cart(View):
    def get(self,request): 
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(product=prod_id,user=request.user)
        if request.GET.get('op') =='minus':
            if c.quantity >1 :
                c.quantity -= 1
                c.save()
        else:
            c.quantity += 1
            c.save()

        carts=Cart.objects.filter(user=request.user)
        total=price_total(c),
        total_amount =total_cart_price(carts)
        data={
                    'quantity':c.quantity,
                    'total':total,
                    'total_amount':total_amount
                }
        return JsonResponse(data)

'''
This Function is Used to Add the products into the Carts.
'''
class AddToCartView(View):
   def get(self,request,id): 
        product= Product.objects.get(id=id)
        product_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=self.request.user)).exists()
        if not product_already_in_cart:
            cart=Cart(user=self.request.user,product=product).save()
        WishList.objects.filter(Q(product=product.id) & Q(user=self.request.user)).delete()
        request.session['total'] = Cart.objects.filter(user=request.user).count()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))

   
'''
This function is Used to remove the products from the cart.
'''
class RemoveCartItemView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart')
        id = self.kwargs['pk']
        if id in cart:
            del cart[id]  
            request.session["cart"] = cart
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



'''
BrainTreee payment GateWay.
'''

Merchant_ID ='f49w49kxcr7dhx3p'
Public_Key='5g29t22hfk42zk2d'
Private_Key='b252c6e805ae98e5735610fdb76eda8e'

# Configuring the environment and API credentials
# Source: https://developer.paypal.com/braintree/docs/start/hello-server/python
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id=Merchant_ID,
        public_key=Public_Key,
        private_key=Private_Key
    )
)

# pass client_token to your front-end
def generate_client_token():
    return str(gateway.client_token.generate())

def transact(options):
    return gateway.transaction.sale(options)

def find_transaction(id):
    return gateway.transaction.find(id)


def pay(request):
    return render(request, 'products/success.html')


def create_checkout(request):
    result = transact({
            'amount': request.POST.get('amount'),
            'payment_method_nonce': request.POST.get('payment_method_nonce'),
            'options': {
            "submit_for_settlement": True
        }
    })
    if result.is_success or result.transaction:
        return render(request, 'products/tr_show.html',{'transaction_id':result.transaction.id} )
        # return redirect(url_for('tr_show',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: 
            print(f'Error: {x.code}: {x.message}')
        return render(request, 'products/braintree.html' )
        
        # return redirect(url_for('tr_new'))


def tr_refund(transaction_id):
    # retrieving the transaction
    transaction = gateway.transaction.find(transaction_id)
    
    # if the transaction is on status settled or settling we refund
    if transaction.status == 'settled' or transaction.status == 'settling':
        result = gateway.transaction.refund(transaction_id)
        # Let's keep errors in the Terminal for this project example
        if result.is_success:
            print("Transaction successfully refunded.")
        else:
            print(f"Could not refund, error: {result.errors.deep_errors}")        
    return redirect(request,'products/tr_show', {'transaction_id':transaction_id})


def tr_refund(transaction_id):
    transaction = gateway.transaction.find(transaction_id)
    
    if transaction.status == 'settled' or transaction.status == 'settling':
        result = gateway.transaction.refund(transaction_id)
        if result.is_success:
            print("Transaction successfully refunded.")
        else:
            print(f"Could not refund, error: {result.errors.deep_errors}")        
    return render(request,'products/tr_show', {'transaction_id':transaction_id})


# Void a transaction
def tr_void(request,transaction_id):
    transaction = gateway.transaction.find(transaction_id)
    
    if transaction.status == 'authorized' or transaction.status == 'submitted_for_settlement' or transaction.status == ' settlement_pending':
        result = gateway.transaction.void(transaction_id)
        if result.is_success:
            print("Transaction successfully voided.")
        else:
            print(f"Could not void the transaction, error: {result.errors.deep_errors}")
    return render(request,'products/tr_show', {'transaction_id':transaction_id})


'''
This function is takes the all the information of billing address ,payment method ,ordererd product and
 checkout the product .
'''
@method_decorator(csrf_exempt, name='dispatch')
class CheckOutView(View):
    def get(self,*args):
        total = self.request.session.get('total')
        payment_methods = PaymentGateway.objects.all()
        userinfo = CustomUserModel.objects.get(id=self.request.user.id)
        adress = UserProfile.objects.get(user=self.request.user,default=True)
        context =  {'total':total,'userinfo':userinfo,'payment_methods' :payment_methods,
                    'adress':adress,'form':CheckoutForm()}
        return render(self.request, 'products/checkout4.html', context)
    
    def post(self,request,*args):
        form = CheckoutForm(request.POST)
        payment_methods = PaymentGateway.objects.all()
        carts=Cart.objects.filter(user=request.user)
        if carts:
            if form.is_valid():         
                fm = form.save(commit=False)
                fm.user =request.user
                fm.grand_total=total_cart_price(carts)
                fm.save()
                order = CustomerOrder.objects.filter(user=self.request.user).last()
                email = order.email
                if request.POST.get('payment_gateway') == '4' or request.POST.get('payment_gateway') == '5':
                    pass
                else:
                    Cart.objects.filter(user = request.user).delete()

                for cart in carts:
                    orderdetails = OrderDetails.objects.create(order=order, product=cart.product, quantity=cart.quantity, amount=cart.product.price)
                if request.POST.get('payment_gateway') == '1':
                    # order_placed_mail(payment)
                    return render(request, 'products/order2.html', {'order':(CustomerOrder.objects.filter(user=request.user,status =True)).last()})

                if request.POST.get('payment_gateway') == '2':
                    context ={'order':21}
                    messages.success(request, 'Order Placed',context)
                    # return render(request, 'products/paypal.html', {'orders':orders, 'total': order.grand_total})
                    return render(request, 'products/paypal.html')

                if request.POST.get('payment_gateway') == '3':
                    client = razorpay.Client(auth = ('rzp_test_tGeRzPBvdwllWI', 'Ro7IdrUx7zZ8TiN3vin2jqcj'))                        
                    payment = client.order.create({'amount': int(total_cart_price(carts)) *100, 'currency': 'INR', 'payment_capture':1})
                    order_placed_mail(email,payment)
                    return render(request, 'products/razorpay.html',{'client':client,'payment':payment})
                    
                if request.POST.get('payment_gateway') == '5':
                    client_token = str(generate_client_token())
                    return render(request, 'products/braintree.html',{'client_token':client_token})

                if request.POST.get('payment_gateway') == '4':
                    return render(request, 'products/stripe.html',{'total':total_cart_price(carts)})

            context =  {'payment_methods' :payment_methods,'form':form}

            return render(self.request, 'products/checkout4.html', context)
        else:
            return render(self.request, 'products/cart.html')
        
    


def PaymentDone(request):
    transaction=request.GET.get('t_id')
    fm =CustomerOrder.objects.get(status=False)
    fm.transaction_id=transaction
    fm.status=True
    fm.save()
    return render(request, 'products/order2.html', {'order':(CustomerOrder.objects.filter(user=request.user,status =True)).last()})


def paymentcomplete(request):
    order =CustomerOrder.objects.get(status=False)
    order.transaction_id= request.GET.get('t_id')
    return render(request, 'products/order_placed.html')


def address(request):
    Order.objects.get(id=request.POST.get('custid'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)


def addwishlist(request,id=None):
    product = Product.objects.get(id=id)
    user = request.user
    product_already_in_wishlist = WishList.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    if product_already_in_wishlist:
        pass
    else:
        WishList(user=user,product=product).save()
    return redirect(showwishlist)

class removewishlist(View):
    def get(self,request,id): 
        remove_item = WishList.objects.get(Q(product=id) & Q(user=request.user)).delete()
        return render(request,'products/wishlist.html')

@login_required(login_url='login')
def showwishlist(request):
    if request.user.is_authenticated:
            user = request.user
            products = WishList.objects.filter(user=user)
            wishlist_product = [ p for p in WishList.objects.all() if p.user == user]
            if wishlist_product:
             return render(request,'products/wishlist.html',{'products':products})
            else:
              return render(request,'products/emptywishlist.html')

'''
Strip integrations with Django.
'''
from django.conf import settings
import stripe

class pay_success(View):
    def get(self,request):
        return render(request, 'products/success.html')

class pay_cancel(View):
    def get(self,request):
        return render(request, 'products/cancel.html')


def PaymentDone(request):
    data = {'t_id':request.GET.get('t_id')}
    order = CustomerOrder.objects.filter(user=request.user).last()
    order.transaction_id = request.GET.get('t_id')
    order.save()
    return JsonResponse(data)

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


class CreateCheckoutSessionView(View):
    def post(self,request,*args,**kwargs):
        host = 'http://127.0.0.1:8000'
        order_id = self.request.POST.get('order-id')
        carts=Cart.objects.filter(user=request.user)
        total = total_cart_price(carts)
        checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
         line_items=[
            {
            'price_data':{
            'currency':'inr',
            'unit_amount':int(total)*100,
            'product_data':{
            'name':'T-shirt',
            'name':123,
                },
            },
            'quantity':1,
         },
         ],
        mode = 'payment',
        success_url = f'{host}/products/success',
        cancel_url = f'{host}/products/cancel',
        )
        return redirect(checkout_session.url, code=303)



@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Passed signature verification
    # return HttpResponse(status=200)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        if session.payment_status == 'paid':
            line_item = session.list_items(session.id, limit=1).data[0]
            # order_id = line_item['description']
            # fulfill_order(order_id)
            fulfill_order(session) 


    # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(order_id):

    order = Order.objects.get(id=order_id)
    order.ordered = True
    order.orderDate = datetime.datetime.now()
    order.save()
    print("Fulfilling order") 





'''
This function will show the matching product in list of index page and shows the matching records.
'''

class searchproduct(ListView):
    template_name = "accounts/product_list.html"  
    paginate_by = 2

    '''
    Here the model manger written.
    '''
    def get_queryset(self):
        return Product.objects.search(self.request.GET.get('search',''))


'''
This View is responsible for the current user recored history of product which he has buy from website.
'''
class Order_History(TemplateView):
    template_name = 'products/order_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
           'order_history':OrderDetails.objects.filter(order__user=self.request.user)
        }
        return context
    

'''
This Function is about the product status and info about product will show and 
using awb number we can track a perticular orderdetails.
'''
class Tracking_Order(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        return render(request,"products/track.html")

    def post(self,request):
        awb = request.POST.get('awb')
        update = OrderDetails.objects.filter(order__awb_no =awb,order__user=request.user)
        updates = []
        [updates.append(order) for order in update ]
        return render(request,"products/track.html",{'updates':updates})