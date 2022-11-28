from django.contrib.auth import logout,login
from django.shortcuts import redirect

'''
This is The middleware Written For the Authantication .it checks Whether user is valid 
or not and return to the response. 
'''
def auth_middleware(get_response):
    def middleware(request):
        if not request.session.get('user'):
            return redirect('login')    
        response = get_response(request)
        return response

    return middleware