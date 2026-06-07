from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Wowtube'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [instance.email]

        html_content = render_to_string(
            'welcome.html',
            {'user': instance}
        )

        text_content = f'Hi {instance.username}, Thank you for Registering'

        email = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            to_email
        )

        email.attach_alternative(html_content, "text/html")
        email.send()