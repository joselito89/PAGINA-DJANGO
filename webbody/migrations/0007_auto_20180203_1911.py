# Generated by Django 2.0.1 on 2018-02-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webbody', '0006_categoriahilo_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriahilo',
            name='imagen',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='webbody/static/images'),
        ),
    ]