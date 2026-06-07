from django.dispatch import Signal, receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

# 🔔 Custom signal
rental_success = Signal()


@receiver(rental_success)
def send_rental_email(sender, **kwargs):
    rental = kwargs.get("rental")

    if not rental:
        return

    user = rental.user

    # Decide content
    if rental.movie:
        content_name = str(rental.movie)
        content_type = "Movie"
    elif rental.webseries:
        content_name = str(rental.webseries)
        content_type = "Web Series"
    else:
        return

    subject = f'{content_type} Rental Successful 🎬'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    # ✅ Same pattern as your welcome email
    html_content = render_to_string(
        'rent.html',
        {
            'user': user,
            'content_name': content_name,
            'content_type': content_type
        }
    )

    text_content = f'Hi {user.username}, you successfully rented {content_name}'

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to_email
    )

    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("✅ EMAIL SENT")
    except Exception as e:
        print("❌ ERROR:", e)
    print("🔥 RENTAL SIGNAL TRIGGERED")