from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200,)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                               null=True, blank=True,)
    text = models.TextField(max_length=1000,)
    likes = models.IntegerField(auto_created=False, )
    dislikes = models.IntegerField(auto_created=False, )
    nested_comment = models.ForeignKey('Comment',
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True,
                                       )

class Image(models.Model):
    title = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='pics')


class Task(models.Model):
    title = models.CharField(max_length=200,)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT,
                                 help_text='Выберите категорию из списка предложенных',)
    author = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=True)
    text = models.TextField(max_length=1000, help_text='Введите условие задачи',)
    answer = models.CharField(max_length=255, help_text='Введите правильный ответ',)
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
    likes = models.IntegerField(auto_created=False,)
    dislikes = models.IntegerField(auto_created=False,)
    image = models.ImageField()
    slug = models.SlugField(max_length=100,)


    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        return reverse('logicaltasks:task_detail', args=[str(self.slug)])

