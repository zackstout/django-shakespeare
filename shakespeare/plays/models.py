from django.db import models

# Create your models here.

class PlayName(models.Model):
    title = models.CharField(max_length=300)
    def __str__(self):
        return self.title

class PlayText(models.Model):
    play = models.ForeignKey(PlayName, on_delete=models.CASCADE)
    act = models.IntegerField(default=0)
    scene = models.IntegerField(default=0)
    lineno = models.IntegerField(default=0)
    speaker = models.CharField(max_length=100)
    text = models.CharField(max_length=300)
    def __str__(self):
        return self.text
