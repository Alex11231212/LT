from django.test import TestCase
from django.utils.text import slugify

from ..models import Task


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        title = 'task1'
        Task.objects.create(
            title=title,
            text='text',
            answer='answer',
            difficulty='u',
            slug=title
        )

    def test_title_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_answer_label(self):
        task = Task.objects.get(id=1)
        field_label = task._meta.get_field('answer').verbose_name
        self.assertEqual(field_label, 'answer')

    def test_title_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_text_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('text').max_length
        self.assertEqual(max_length, 1000)

    def test_answer_max_length(self):
        task = Task.objects.get(id=1)
        max_length = task._meta.get_field('answer').max_length
        self.assertEqual(max_length, 1000)

    def test_object_name_is_title(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task.title}'
        self.assertEqual(str(task.slug), expected_object_name)

    def test_slug_is_title(self):
        task = Task.objects.get(id=1)
        expected_object_name = f'{task.title}'
        self.assertEqual(str(task), expected_object_name)

    def test_get_absolute_url(self):
        task = Task.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(task.get_task_url(), '/lt/task/task1/')

