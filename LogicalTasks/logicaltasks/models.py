from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# class Category(models.Model):
#     name = models.CharField(max_length=200,)
#
#     def __str__(self):
#         """String for representing the Model object."""
#         return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, blank=True,)
    text = models.TextField(max_length=1000,)
    likes = models.IntegerField(auto_created=False, default=0)
    dislikes = models.IntegerField(auto_created=False, default=0)
    nested_comment = models.ForeignKey('Comment',
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True,
                                       )


class Image(models.Model):
    title = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='pics')

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class ImageAnswer(models.Model):
    title = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='pics')

    def __str__(self):
        """String for representing the Model object."""
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=200,)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               blank=True, null=True,)
    text = models.TextField(max_length=1000, help_text='Введите условие задачи',)
    answer = models.TextField(max_length=1000, blank=True,
                              help_text='Введите правильный ответ',)
    image_answer = models.ForeignKey(ImageAnswer, blank=True,
                                     null=True,
                                     on_delete=models.SET_NULL,
                                     help_text='Выберите картинку - ответ',)
    DIFFICULTY_LEVEL = (
        ('e', 'Easy'),
        ('m', 'Medium'),
        ('h', 'Hard'),
        ('u', 'Undefined'),
    )
    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_LEVEL,
        default='u',
        help_text='Сложность задачи',
    )
    likes = models.IntegerField(auto_created=False, default=0)
    dislikes = models.IntegerField(auto_created=False, default=0)
    image = models.ForeignKey(Image, blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              help_text='Выберите картинку для задачи с иллюстрацией',)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_task_url(self):
        return reverse('logicaltasks:task_detail', args=[str(self.slug)])

