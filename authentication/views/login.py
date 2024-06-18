from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from authentication.helper import ShouldNotLoggedIn

class Login(ShouldNotLoggedIn, View):
    def get(self, request):
        return render(request, 'authentication/login.html', {})
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        user = authenticate(request, username=email , password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request,'authentication/login.html', {'email':email,'password':password})