# signals to lock the account and register the login activity.
from authentication.models import AuthenticationLog
from django.contrib.auth import get_user_model, user_login_failed, user_logged_in
from django.dispatch import receiver
from django.contrib import messages

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_login_failed)
def login_failed(sender, credentials, request, **kwargs):
    """Deactive account on 3 failed attempt"""
    email = credentials.get('username')
    try:
        User = get_user_model()
        user = User.objects.get(email=email)
        if user.login_failed_attempt >= 3 :
            # deactive the account.
            user.is_active = False
            user.save()
            messages.error(request, 'Your account is locked, kindly unlock your account.')
        else:
            user.login_failed_attempt += 1
            user.save()
            messages.error(request, 'Your credentail is wrong')
        # logging the failed activity
        AuthenticationLog.objects.create(
            email = email,
            ip_address = get_ip_address(request),
            is_success = False,
        )
    except:
        # catch all the error, don't do anything.
        pass


@receiver(user_logged_in)
def post_login(sender, request, user, **kwargs):
    # change the counter
    if user.login_failed_attempt != 0 :
        user.login_failed_attempt = 0
        user.save()
    AuthenticationLog.objects.create(
        email = user.email,
        ip_address = get_ip_address(request),
        is_success = True,
    )
        