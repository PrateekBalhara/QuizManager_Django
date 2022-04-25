from django.contrib import admin
from .models import Quiz, Question, User, Result

# Registered all tables here to access them in Django Admin
# All Data was added and modified using Django Admin

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_admin = ['topic']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'statement', 'options', 'answer']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass