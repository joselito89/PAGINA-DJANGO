# Generated by Django 2.0.1 on 2018-02-05 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webbody', '0013_auto_20180204_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='id',
        ),
        migrations.AlterField(
            model_name='perfil',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
