from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_welcome_email(user_email, user_name):
    subject = "Welcome to Showcase! 🎉🎉"
    html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; color: #333;">
                <strong>Hi {user_name},</strong>
                <p style="font-size: 16px; margin-bottom: 16px;">
        Welcome to <strong>Showcase</strong> – a platform created to give you a firsthand look at the potential of <strong>Python</strong> and <strong>Django</strong>! I'm excited to share this journey with you.
            </p>
            <p style="font-size: 16px; margin-bottom: 16px;">
                Thank you for signing up! This project was designed to demonstrate my expertise in Python and Django, allowing you to experience a user-friendly environment where professionals can connect, explore projects, and find opportunities.
            </p>
                <p style="font-size: 16px; color: #555;">
                    Best regards,<br />
                    <strong>Ardhendu Sekhar Sahoo</strong>
                </p>
            </body>
            </html>
        """
    from_email = settings.EMAIL_HOST_USER
# Sending the email with only HTML content
    email = EmailMessage(
        subject, html_message, from_email, [user_email]
    )
    email.content_subtype = "html"  # This sets the content type to HTML
    email.send()