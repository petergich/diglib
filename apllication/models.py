from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os
class Archive_owner(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    username=models.CharField(max_length=254)
    def __str__ (self):
        return self.username
class Archive(models.Model):
    FORMAT_CHOICES = [
        ('PDF', 'PDF'),
        ('Word', 'Word Document'),
        ('JPEG', 'JPEG Image'),
    ]

    GENRE_CHOICES = [
        ('Physics', 'Physics'),
        ('History', 'History'),
        ('Literature', 'Literature'),
        ('Medicine','Medicine'),
        ('Technology','Technology'),
        ('Chemistry','Chemistry'),
        ('Arts','Arts'),
        ('Science','Science'),
        ('Mathematics','Mathematics'),
        ('Computing','Computing'),
    ]

    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Archive_owner, on_delete=models.CASCADE) 
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    file = models.FileField(upload_to='archives/',null = False,blank = False)
    preview_image = models.ImageField(upload_to='previews/',null = False,blank = False)

    def display_preview_image(self):
        if self.preview_image:
            return mark_safe(f'<img src="{self.preview_image.url}" style="max-height:100px;max-width:100px;" />')
        else:
            return 'No Preview Available'

    display_preview_image.short_description = 'Preview'

    def __str__(self):
        return str(self.name)
    
@receiver(pre_delete, sender=Archive)
def delete_archives_media(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
            os.remove(instance.preview_image.path)

class Profile(models.Model):
    TYPE_CHOICES = [
        ('Author','Author'),
        ('Normal User','Normal User')
        ]
    account = models.CharField(max_length =30,choices = TYPE_CHOICES)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=False,default='profile/a.png')

    def display_profile_image(self):
            if self.profile_image:
                return mark_safe(f'<img src="{self.profile_image.url}" style="max-height:100px;max-width:100px;" />')
            else:
                return 'No Preview Available'

    display_profile_image.short_description = 'Preview'


