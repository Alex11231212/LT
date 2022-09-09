from django.contrib import admin

from .models import Task, Image, ImageAnswer
# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'author',
                    'image', 'answer', 'image_answer',
                    'difficulty', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'answer',
                       'difficulty', 'author', 'slug',)
        }),
        ('Images', {
            'classes': ('collapse',),
            'fields': ('image', 'image_answer',)
        }),
    )


admin.site.register(Image)
admin.site.register(ImageAnswer)

