from rest_framework import serializers

from logicaltasks.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'author', 'text',
                  'answer', 'image_answer',
                  'difficulty',
                  'image', 'slug', 'pub_date')
