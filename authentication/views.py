from django.shortcuts import render
from .facade import SocialLoginFacade


def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        #login logic...
        
    return render(request, 'login.html')

def google_login(request):
    facade = SocialLoginFacade('google')
    return facade.login(request)

def google_callback(request):
    facade = SocialLoginFacade('google')
    return facade.callback(request)

def facebook_login(request):
    facade = SocialLoginFacade('facebook')
    return facade.login(request)

def facebook_callback(request):
    facade = SocialLoginFacade('facebook')
    return facade.callback(request)

