from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class News(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)

class NewsImages(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)

class Tags(models.Model):
    tag = models.CharField(max_length=255)
    def __str__(self):
        return self.tag


class NewTags(models.Model):
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

class Anonymous(models.Model):
    token = models.CharField(max_length=255)

class AnonymousFeedback(models.Model):
    anonymous = models.ForeignKey(Anonymous, on_delete=models.CASCADE)
    status = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)],blank=True,null=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)], blank=True, null=True)