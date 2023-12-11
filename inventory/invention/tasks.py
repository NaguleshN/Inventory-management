from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import PurchasedItem
from celery import shared_task

@shared_task(bind=True)
def send_notification_mail(self):
    users = get_user_model().objects.all()

    for user in users:
        purchased_items = PurchasedItem.objects.filter(user=user, date_added__date=timezone.now().date())

        for item in purchased_items:
            mail_subject = "Celery Testing"
            message = "Your due date have been reached!!"
            to_email = user.email

            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False,
            )

    return "Done"