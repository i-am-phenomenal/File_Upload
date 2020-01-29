# Generated by Django 3.0.2 on 2020-01-27 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_upload_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('filepath', models.FileField(null=True, upload_to='file/', verbose_name='')),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]