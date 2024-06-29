
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
import random
from .models import OTP
import requests


def id_generator(size=4, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@receiver(post_save, sender=OTP)
def send_sms(sender, instance, created, **kwargs):
    url = "https://www.kwtsms.com/API/send/"
    username = "paywaysol"
    password = "we5gWPUf!G"
    if created:
        print("Sending SMS to", instance.phone_number)
        code = id_generator()
        params = {
            "username": username,
            "password": password,
            "sender": "KWT-SMS",
            "mobile": instance.phone_number,
            "test": "0",
            "lang": "1",
            "message": f"Your OTP is {code}",
        }
        response = requests.post(url, data=params, verify=True)
        print(response)
        if response.status_code == 200:
            instance.otp = code
            instance.expires_at = instance.created_at + \
                datetime.timedelta(minutes=5)
            instance.save(update_fields=['otp', 'expires_at'])
