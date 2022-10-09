import datetime
import time
import uuid

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.utils import timezone

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from ..models import *
from .. import views


class TaskListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_tasks = 13

        for task_id in range(number_of_tasks):
            title = f'Task_{task_id}'
            Task.objects.create(
                title=title,
                text=f'Text_for_task_{task_id}',
                answer=f'Answer_for_task_{task_id}',
                difficulty='easy',
                slug=title,
            )

    def test_view_url_for_easy_tasks_exists_at_desired_location(self):
        response = self.client.get('/lt/tasks/easy/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_for_medium_tasks_exists_at_desired_location(self):
        response = self.client.get('/lt/tasks/medium/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_for_hard_tasks_exists_at_desired_location(self):
        response = self.client.get('/lt/tasks/hard/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logicaltasks:task_list', kwargs={'level': 'easy'}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('logicaltasks:task_list', kwargs={'level': 'easy'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'logicaltasks/task_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('logicaltasks:task_list', kwargs={'level': 'easy'}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['task_list']), 10)

    def test_lists_all_tasks(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('logicaltasks:task_list', kwargs={'level': 'easy'})+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['task_list']), 3)


class TaskDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        title = 'task_1_for_detail'
        task = Task.objects.create(
            title=title,
            author=User.objects.create_user(
                username='test_user1',
                password='qweAsd$$322!!',
            ),
            text='text_for_task_1',
            answer='answer_for_task_1',
            image_answer=ImageAnswer.objects.create(
                title='image_answer_for_task_1',
                photo='photo_answer.jpg'
            ),
            difficulty='easy',
            image=Image.objects.create(
                title='image_for_task_1',
                photo='photo_answer.jpg'
            ),
            slug=title,
        )

    def test_view_url_for_task_slug(self):
        response = self.client.get('/lt/task/task_1_for_detail/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('logicaltasks:task_detail', kwargs={'task_slug': 'task_1_for_detail'}))
        self.assertEqual(response.status_code, 200)

    def test_view_anonymous_user_cannot_pass_like_on_task(self):
        response = self.client.post(reverse('logicaltasks:task_like', kwargs={'pk': 0}),
                                    {'model': Task,
                                     'vote_type': LikeDislike.LIKE,})
        self.assertEqual(response.status_code, 302)

    def test_view_anonymous_user_cannot_pass_dislike_on_task(self):
        response = self.client.post(reverse('logicaltasks:task_dislike', kwargs={'pk': 0}),
                                    {'model': Task,
                                     'vote_type': LikeDislike.DISLIKE,})
        self.assertEqual(response.status_code, 302)

    def test_view_anonymous_user_cannot_pass_like_on_comment(self):
        response = self.client.post(reverse('logicaltasks:task_like', kwargs={'pk': 0}),
                                    {'model': Comment,
                                     'vote_type': LikeDislike.LIKE,})
        self.assertEqual(response.status_code, 302)

    def test_view_anonymous_user_cannot_pass_dislike_on_comment(self):
        response = self.client.post(reverse('logicaltasks:task_like', kwargs={'pk': 0}),
                                    {'model': Comment,
                                     'vote_type': LikeDislike.DISLIKE,})
        self.assertEqual(response.status_code, 302)