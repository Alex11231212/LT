# Generated by Django 4.0.4 on 2022-09-09 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('photo', models.ImageField(upload_to='pics')),
            ],
        ),
        migrations.CreateModel(
            name='ImageAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('photo', models.ImageField(upload_to='pics')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField(help_text='Введите условие задачи', max_length=1000)),
                ('answer', models.TextField(blank=True, help_text='Введите правильный ответ', max_length=1000)),
                ('difficulty', models.CharField(choices=[('e', 'Easy'), ('m', 'Medium'), ('h', 'Hard'), ('u', 'Undefined')], default='u', help_text='Сложность задачи', max_length=1)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('image', models.ForeignKey(blank=True, help_text='Выберите картинку для задачи с иллюстрацией', null=True, on_delete=django.db.models.deletion.SET_NULL, to='logicaltasks.image')),
                ('image_answer', models.ForeignKey(blank=True, help_text='Выберите картинку - ответ', null=True, on_delete=django.db.models.deletion.SET_NULL, to='logicaltasks.imageanswer')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('likes', models.IntegerField(default=0)),
                ('dislikes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('nested_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='logicaltasks.comment')),
            ],
        ),
    ]