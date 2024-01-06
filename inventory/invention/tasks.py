from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import PurchasedItem
from celery import shared_task
from datetime import datetime, timedelta

@shared_task(bind=True)
def send_notification_mail(self):
    users = get_user_model().objects.all()

    for user in users:
        purchased_items = PurchasedItem.objects.filter(user=user, due_date__date=timezone.now().date())

        for item in purchased_items:
            mail_subject = "Due mail"
            message = "Your due_date has been crossed. So, return your products today."
            to_email = user.email

            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False,
            )
            item.email_sent = True
            item.save()

    return "Done"

@shared_task(bind=True)
def send_warning_mail(self):
    try:
        users = get_user_model().objects.all()

        for user in users:
            purchased_items = PurchasedItem.objects.filter(
                user=user,
                due_date__date=timezone.now().date() + timedelta(days=2),
            )

            for item in purchased_items:
                warning_date = item.due_date - timedelta(days=2)
                if timezone.now().date() >= warning_date.date():
                    mail_subject = "Warning mail"
                    message = "Your due date is going to reach in 2 days. Please return your respective products."
                    to_email = user.email

                    send_mail(
                        subject=mail_subject,
                        message=message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[to_email],
                        fail_silently=True,
                    )
                    print(f"Warning mail sent to {to_email}")
                    
                    item.email_sent = True
                    item.save()

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False