from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@shared_task
def send_email(template_name, context, subject, to_args):
    html_body = render_to_string(template_name, context)
    email_msg = EmailMultiAlternatives(
        subject=subject,
        from_email= settings.DEFAULT_EMAIL,
        to = to_args, 
        body = html_body
    )
    email_msg.attach_alternative(html_body, "text/html")
    email_msg.send()
    return "email sent successfully with msg : " + str(subject)