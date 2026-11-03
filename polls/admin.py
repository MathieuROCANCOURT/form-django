from django.contrib import admin
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date"]
    list_filter = ["question_text"]
    ordering = ["pub_date"]
    search_fields = ["question_text"]


admin.site.register(Choice)
admin.site.register(Question, QuestionAdmin)
