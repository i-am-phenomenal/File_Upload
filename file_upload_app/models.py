from django.db import models

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
    # fname = models.CharField(max_length=200)
    # lname = models.CharField(max_length=200)
    # technologies = models.CharField(max_length=500)
    # email = models.EmailField(default=None)
    music_file = models.FileField()
    music_name = models.CharField(max_length=200)

    def __str__(self):
        return self.music_name
