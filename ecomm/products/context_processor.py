from .models import Cart
'''
This context processor we use  when you need to make something available globally to all templates.
It will Shows the all the Count of cart in evry template.
'''
def Cart_Count(request):
    if  request.user.is_authenticated:
        totalitem=Cart.objects.filter(user = request.user).count()
        return {'cart':totalitem}
    return {}
