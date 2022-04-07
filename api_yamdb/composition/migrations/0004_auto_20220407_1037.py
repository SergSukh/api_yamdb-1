# Generated by Django 2.2.16 on 2022-04-07 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('composition', '0003_genres_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titles',
            name='genres',
        ),
        migrations.AddField(
            model_name='titles',
            name='genre',
            field=models.ForeignKey(blank=True, help_text='Введите жанр произведения', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='titles', to='composition.Genres', verbose_name='Жанры'),
        ),
        migrations.DeleteModel(
            name='GenreTitle',
        ),
    ]
