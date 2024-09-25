from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from urllib.parse import urlparse

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    total_videos = models.PositiveIntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name



class Article(models.Model):
    course_name = models.ForeignKey('Course', on_delete=models.CASCADE)
    article_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    article_video_url = models.URLField(blank=True, null=True)
    article_video_thumbnail = models.URLField(blank=True, null=True)
    hyperlinks = models.ManyToManyField('Hyperlink', related_name='articles', blank=True)
    contents = models.ManyToManyField('Content', related_name='articles', blank=True)
    quiz = models.ManyToManyField('Quiz', related_name='article_quizzes', blank=True)

    def get_youtube_video_id(self, url):
        """
        Extracts YouTube video ID from a URL.
        Supports regular, short, and embed YouTube URLs.
        """
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc and 'v=' in parsed_url.query:
            return parsed_url.query.split('v=')[1].split('&')[0]
        elif 'youtu.be' in parsed_url.netloc:
            return parsed_url.path.split('/')[1]
        elif 'youtube.com' in parsed_url.netloc and '/embed/' in parsed_url.path:
            return parsed_url.path.split('/embed/')[1].split('?')[0]
        return None

    def get_youtube_thumbnail_url(self, video_id):
        """
        Returns the YouTube thumbnail URL for a given video ID.
        """
        return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

    def save(self, *args, **kwargs):
        # Generate slug if it's not provided
        if not self.slug:
            self.slug = slugify(self.article_name)

        # If there's a YouTube video URL, generate the thumbnail
        if self.article_video_url:
            video_id = self.get_youtube_video_id(self.article_video_url)
            if video_id:
                self.article_video_thumbnail = self.get_youtube_thumbnail_url(video_id)
            else:
                print("Error: Could not extract YouTube video ID from the URL.")

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_name


class Hyperlink(models.Model):
    article_name = models.ForeignKey(Article, related_name='hyperlinks_set', blank=True, null=True,on_delete=models.CASCADE)
    hyper_link_word = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    hyper_link_word_url = models.URLField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.hyper_link_word)
        super(Hyperlink, self).save(*args, **kwargs)

    def __str__(self):
        return self.hyper_link_word


class Content(models.Model):
    content_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, related_name='content', on_delete=models.CASCADE) 

    content_name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.content_name


class VideoPlayer(models.Model):
    video_played_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, related_name='videos', on_delete=models.CASCADE)
    video_title = models.CharField(max_length=255)
    video_description = models.TextField()
    channel_name = models.CharField(max_length=100)

    def __str__(self):
        return self.video_title



class Quiz(models.Model):
    article = models.ForeignKey(Article, related_name='quizzes', on_delete=models.CASCADE)
    question = models.TextField()
    options = models.TextField(help_text="Separate each option with a comma")
    opt_values = models.TextField(help_text="Enter the option values corresponding to each option, separated by semicolon")
    correct_options = models.TextField(help_text="Enter the correct options separated by semicolon")

    def __str__(self):
        return f"Quiz for {self.article_name}"


# class UserPerformance(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name='course',on_delete=models.CASCADE)
#     watched_videos = models.ManyToManyField(VideoPlayer)

#     def __str__(self):
#         return f"Performance of {self.user.username}"



class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course',null=True, on_delete=models.CASCADE)
    watched_videos = models.ManyToManyField(VideoPlayer)

    @property
    def progress(self):
        total_videos = self.course.total_videos
        watched_videos_count = self.watched_videos.count()
        if total_videos > 0:
            return (watched_videos_count / total_videos) * 100
        return 0  # If no videos in the course

    def __str__(self):
        return f"Performance of {self.user.username}"

