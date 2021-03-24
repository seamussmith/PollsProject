from django.contrib import admin
from .models import *

# Register your models here.
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question']
    list_display = (
        "question",
        "pub_date",
    )
    fieldsets = [
        ('Question', {
            'fields': ['question']
        }),
        ('Date', {
            'fields': ['pub_date']
        }),
        ('UUID', {
            'fields': ['uuid']
        })
    ]
    inlines = [
        ChoiceInline
    ]

admin.site.register(Poll, QuestionAdmin)
admin.site.register(Choice)
