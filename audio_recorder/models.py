from django.db import models


class EnglishTranscipt(models.Model):
    text = models.TextField()


class HindiTranscipt(models.Model):
    text = models.TextField()


class TamilTranscipt(models.Model):
    text = models.TextField()


class User(models.Model):
    full_name = models.CharField(max_length=50)


class SpeechData(models.Model):
    aws_link = models.URLField()
    base64 = models.TextField()
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='speech_data')
