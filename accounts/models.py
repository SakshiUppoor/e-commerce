from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    profile_images = models.ImageField(
        default="profile_images/default.jpg", upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        if self.is_company:
            return self.first_name
        elif self.is_customer:
            return self.first_name+" "+self.last_name
        else:
            return self.username


class Company(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name="company")
    description = models.CharField(max_length=255, blank=True, null=True)
    header = models.ImageField(
        default="headers/default.jpg", upload_to='headers', blank=True, null=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "companies"


@receiver(post_save, sender=User)
def create_companies(sender, **kwargs):
    if kwargs['created'] and kwargs.get('instance').is_company == True:
        company = Company.objects.create(user=kwargs.get('instance'))
