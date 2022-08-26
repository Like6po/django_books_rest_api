from celery import shared_task
from django.core.mail import send_mail

from books_app.settings import EMAIL_HOST_USER


@shared_task()
def send(subject: str, message: str, recipient: str):
    send_mail(subject=subject,
              message=message,
              from_email=EMAIL_HOST_USER,
              recipient_list=[recipient],
              )
