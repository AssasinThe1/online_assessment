from django.contrib import admin
from .models import Question, Choice, Test, Submission


admin.site.register(Choice)
admin.site.register(Test)
admin.site.register(Submission)
admin.site.register(Question)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # Number of extra empty choice fields

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

