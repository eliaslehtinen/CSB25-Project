from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    note_name = models.CharField(max_length=30)
    created_date = models.DateTimeField()
    note_content = models.CharField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Note: " + self.note_name