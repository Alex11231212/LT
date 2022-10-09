import datetime

from django.test import TestCase, SimpleTestCase
from django.utils import timezone

from ..forms import CommentForm


class CommentFormTest(SimpleTestCase):
    def test_renew_form_date_field_label(self):
        text = '   '
        form = CommentForm(data={'text': text})
        self.assertFalse(form.is_valid())
