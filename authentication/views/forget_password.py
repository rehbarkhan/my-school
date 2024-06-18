from django.views import View
from authentication.helper import ShouldNotLoggedIn
from django.shortcuts import render
from django.utils.crypto import get_random_string
from authentication.models import AccountRecovery
from django.utils import timezone
from authentication.tasks import send_email

class ForgetPassword(ShouldNotLoggedIn, View):
    def get(self, request):
        return render(request, 'authentication/forget-password.html', {})
    
    def post(self, request):
        if request.htmx : 
            email = request.POST.get('email')
            try:
                account = AccountRecovery.objects.get(email = email,is_forget = True, token_validity_till__gte =  timezone.now())
            except:
                account = AccountRecovery.objects.create(email=email, is_forget = True)
            context = {
                'email': account.email,
                'token': account.token
            }
            send_email.delay('authentication/email/forget-password-email.html', context, "Password reset request", [context.get('email')])
            return render(request, 'authentication/partials/_auth-success.html', {'msg':"Successfully sent the email wiht the password reset link."})
        return self.get(request)