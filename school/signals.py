from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from school.models import Bracelet, Student, Teacher
from wallet.models.wallet import Wallet


@receiver(post_save, sender=Bracelet)
def update_wallet(sender, instance, created, **kwargs):
    if instance.status == Bracelet.ACTIVE:
        try:
            wallet = Wallet.objects.get(bracelet=instance)
            wallet.active = True
            wallet.save()
        except Wallet.DoesNotExist:
            Wallet.objects.create(bracelet=instance)
            instance.wallet.save()
    elif instance.status == Bracelet.DEACTIVATED:
        try:
            wallet = instance.wallet
            wallet.active = False
            wallet.save()
        except Wallet.DoesNotExist:
            pass
    elif instance.status == Bracelet.UNASSIGNED:
        try:
            with transaction.atomic():
                student = Student.objects.get(bracelet=instance)
                student.bracelet = None
                wallet = Wallet.objects.get(bracelet=instance)
                wallet.delete()
                student.save()
        except Student.DoesNotExist:
            pass
        except Wallet.DoesNotExist:
            pass
        try:
            with transaction.atomic():
                teacher = Teacher.objects.get(bracelet=instance)
                teacher.bracelet = None
                wallet = Wallet.objects.get(bracelet=instance)
                wallet.delete()
                teacher.save()
        except Teacher.DoesNotExist:
            pass
        except Wallet.DoesNotExist:
            pass
