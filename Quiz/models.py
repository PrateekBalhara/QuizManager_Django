from datetime import datetime

from django.db import models

# Model to store all Users
class User(models.Model):
    name = models.CharField(max_length=50)
    college_id = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    # String representation for the object
    def __str__(self):
        return self.name

# Model to store all quiz topics
class Quiz(models.Model):
    topic = models.CharField(max_length=100)
    duration = models.IntegerField()

    def __str__(self):
        return self.topic

# Class Model to store questions for all quiz topics
class Question(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    statement = models.TextField()
    options = models.TextField()
    answer = models.IntegerField()

    # Splits the options and returns a list of options
    def options_as_list(self):
        return self.options.split(";")

    def __str__(self):
        return self.statement

# Class Model to store all user results in quizes
class Result(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    score = models.IntegerField()
    entry_time = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return str(self.quiz) + "- " + str(self.user) + ": " + str(self.score)


