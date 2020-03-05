from django.db import models
import os 
import uuid 

# Create your models here.


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title


class File(models.Model):
    name = models.CharField(max_length=500)
    filepath = models.FileField(upload_to='file/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.filepath)


class User_Profile(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    music_file = models.FileField()
    music_name = models.CharField(max_length=200)
    extension = models.CharField(max_length=10, default='mp3', editable=False)
   

    def __str__(self):
        return self.music_name

    def return_file_name(self):
        return os.path.basename(self.music_file.name)
