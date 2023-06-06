# Generated by Django 4.1.5 on 2023-05-05 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fec_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Actua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vimad_app.actor')),
            ],
        ),
        migrations.CreateModel(
            name='Corto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('puntuacion', models.IntegerField()),
                ('genero', models.CharField(max_length=50)),
                ('duracion', models.CharField(max_length=3)),
                ('fec_estreno', models.DateField()),
                ('idioma', models.CharField(max_length=50)),
                ('pais', models.CharField(max_length=50)),
                ('sinopsis', models.TextField(max_length=300)),
                ('imagen', models.CharField(default='', max_length=100)),
                ('video', models.CharField(default='', max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, unique=True)),
                ('actor', models.ManyToManyField(through='vimad_app.Actua', to='vimad_app.actor')),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fec_nacimiento', models.DateField()),
                ('nacionalidad', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Estudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('fec_fundacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Dirige',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('corto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vimad_app.corto')),
                ('director', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vimad_app.director')),
            ],
        ),
        migrations.AddField(
            model_name='corto',
            name='director',
            field=models.ManyToManyField(through='vimad_app.Dirige', to='vimad_app.director'),
        ),
        migrations.AddField(
            model_name='corto',
            name='estudio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vimad_app.estudio'),
        ),
        migrations.AddField(
            model_name='actua',
            name='corto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vimad_app.corto'),
        ),
    ]
