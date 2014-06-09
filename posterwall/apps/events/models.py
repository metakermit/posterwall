from django.db import models

# Create your models here.
class Event(models.Model):
    url = models.URLField(null=True)
    img_url = models.URLField(null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title
