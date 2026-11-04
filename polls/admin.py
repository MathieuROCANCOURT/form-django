from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    list_filter = ["question_text"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ["question__question_text", "choice_text", "votes"]
    list_filter = ["question", "choice_text"]
    ordering = ["question", "votes"]
    search_fields = ["question", "choice_text"]


admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Question, QuestionAdmin)
