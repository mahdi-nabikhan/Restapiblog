from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


@shared_task
def send_activation_email(user_email, user_name, access_token):
    message_body = f"""
        Hello {user_name},

        Here is your JWT access token:
        {access_token}

        If you did not request this, please ignore this email.
    """
    email_message = EmailMessage(
        subject="Your Access Token",
        body=message_body,
        from_email="noreply@example.com",
        to=[user_email]
    )
    email_message.send()


@shared_task
def send_activation_confirmation_email(user_email, user_name):
    context = {
        'user_name': user_name,
    }
    message_body = render_to_string('email/activation_email.tpl', context)
    email_message = EmailMessage(
        subject="Your Account Has Been Activated",
        body=message_body,
        from_email="noreply@example.com",
        to=[user_email]
    )
    email_message.content_subtype = 'html'
    email_message.send()
