from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name


class Article(models.Model):
    course_name = models.ForeignKey(Course, on_delete=models.CASCADE)
    article_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    article_video_thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    article_video_url = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article_name)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_name


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    content_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.content_name


class VideoPlayer(models.Model):
    video_played_id = models.AutoField(primary_key=True)
    article_video_url = models.ForeignKey(Article, related_name='videos', on_delete=models.CASCADE)
    article_video_thumbnail = models.ForeignKey(Article, related_name='thumbnails', on_delete=models.CASCADE)
    video_title = models.CharField(max_length=255)
    video_description = models.TextField()
    channel_name = models.CharField(max_length=100)

    def __str__(self):
        return self.video_title


class Quiz(models.Model):
    article_name = models.ForeignKey(Article, related_name='quizzes', on_delete=models.CASCADE)
    question = models.TextField()
    options = models.TextField(help_text="Separate each option with a comma")
    opt_values = models.TextField(help_text="Enter the option values corresponding to each option, separated by commas")
    correct_options = models.TextField(help_text="Enter the correct options separated by commas")

    def __str__(self):
        return f"Quiz for {self.article.article_name}"


class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watched_videos = models.ManyToManyField(VideoPlayer)

    def __str__(self):
        return f"Performance of {self.user.username}"
