# Generated by Django 4.1.2 on 2022-12-19 05:06

import ckeditor.fields
import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Pin', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
                ('Title', models.CharField(blank=True, max_length=255, null=True)),
                ('Description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]