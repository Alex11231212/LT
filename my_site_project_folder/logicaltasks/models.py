from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
        ('undefined', 'Undefined'),
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVEL,
        default='undefined',
        help_text='Сложность задачи',
    )
    reaction = GenericRelation('LikeDislike', related_query_name='tasks')
    image = models.ForeignKey(Image, blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              help_text='Выберите картинку для задачи с иллюстрацией',)
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name='URL')
    pub_date = models.DateField(default=timezone.now)
    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_task_url(self):
        return reverse('logicaltasks:task_detail',
                       kwargs={
                           'task_slug': self.slug,
                       }
                       )


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,)
    text = models.TextField(max_length=1000, blank=True)
    reaction = GenericRelation('LikeDislike', related_query_name='comments')
    nested_comment = models.ForeignKey('Comment',
                                       on_delete=models.CASCADE,
                                       blank=True,
                                       null=True,
                                       )
    pub_date = models.DateField(default=timezone.now)


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # We take the queryset with records greater than 0
        return self.get_queryset().filter(vote__gt=0)

    def dislikes(self):
        # We take the queryset with records less than 0
        return self.get_queryset().filter(vote__lt=0)

    def sum_rating(self):
        # We take the total rating
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0

    def comments(self):
        return self.get_queryset().filter(
            content_type__model='comment').order_by('-comments__pub_date')


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1

    VOTES = (
        (DISLIKE, 'Dislike'),
        (LIKE, 'Like')
    )

    vote = models.SmallIntegerField(verbose_name=_("Голос"), choices=VOTES)
    user = models.ForeignKey(User, verbose_name=_("Пользователь"),
                             on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


