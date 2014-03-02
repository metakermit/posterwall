from django.db import models

# Create your models here.
class Event(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
