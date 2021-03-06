# Generated by Django 2.0.1 on 2018-02-04 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webbody', '0009_categoriahilo_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='máximo 100 caracteres', max_length=100)),
                ('portada', models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/')),
                ('size', models.FloatField()),
                ('descripcion', models.CharField(help_text='máximo 300 caracteres', max_length=300)),
                ('enlace', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webbody.Enlace')),
            ],
        ),
        migrations.RenameField(
            model_name='hilos',
            old_name='comen',
            new_name='comentario',
        ),
        migrations.AlterField(
            model_name='juegos',
            name='portada',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='musica',
            name='portada',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='peliculas',
            name='portada',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='series',
            name='portada',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='imgprincipal',
            field=models.ImageField(default='webbody/static/images/failed.jpg', upload_to='images/'),
        ),
    ]
