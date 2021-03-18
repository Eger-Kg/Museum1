from django.db import models
from django.utils import timezone
from custom_auth.models import User


class Incident(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    incident_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    date = models.CharField(max_length=250)
    info = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'incident'
        verbose_name_plural = 'incidents'

    def __str__(self):
        return self.incident_name


class Advertisement(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.title} - by {self.incident}'


class AdvertisementImage(models.Model):
    advertisement = models.ForeignKey(Advertisement, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ad_image')
    description = models.CharField(max_length=55)

    def __str__(self):
        if self.image:
            return self.image.url
        return ''


class Commentary(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    body = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)