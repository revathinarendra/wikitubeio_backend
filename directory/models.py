from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

import os  

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


AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'ap-north-1')
print(AWS_S3_REGION_NAME)

from .utils.transcription_utils import (
    get_youtube_video_id,
    get_youtube_thumbnail_url,
    download_youtube_audio,
    upload_audio_to_s3,
    start_transcription_job,
    get_transcription_result,
    cleanup_files
)

class Article(models.Model):
    course_name = models.ForeignKey('Course', on_delete=models.CASCADE)
    article_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    article_video_url = models.URLField(blank=True, null=True)
    article_video_thumbnail = models.URLField(blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    hyperlinks = models.ManyToManyField('Hyperlink', related_name='articles', blank=True)
    contents = models.ManyToManyField('Content', related_name='articles', blank=True)
    quiz = models.ManyToManyField('Quiz', related_name='article_quizzes', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.article_name)

        if self.article_video_url:
            video_id = get_youtube_video_id(self.article_video_url)
            if video_id:
                self.article_video_thumbnail = get_youtube_thumbnail_url(video_id)

                # Download and upload the audio
                audio_file = download_youtube_audio(self.article_video_url)
                s3_url = upload_audio_to_s3(audio_file, f'articles/{self.slug}.mp3')

                # Start transcription job
                job_name = f"transcription-{self.slug}"
                try:
                    transcription_text = get_transcription_result(job_name)
                    print(f"Transcription job already exists for {job_name}. Retrieved transcript.")
                except Exception as error:
                    print(f"No existing transcription job found. Starting new job for {job_name}.")
                    start_transcription_job(s3_url, job_name)
                    transcription_text = get_transcription_result(job_name)

                # Save the transcript if available
                if transcription_text:
                    self.transcript = transcription_text

                # Clean up local files
                cleanup_files(audio_file)

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_name

# class Article(models.Model):
#     course_name = models.ForeignKey('Course', on_delete=models.CASCADE)
#     article_name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=200, unique=True)
#     description = models.TextField()
#     article_video_url = models.URLField(blank=True, null=True)
#     article_video_thumbnail = models.URLField(blank=True, null=True)
#     transcript = models.TextField(blank=True, null=True)
#     hyperlinks = models.ManyToManyField('Hyperlink', related_name='articles', blank=True)
#     contents = models.ManyToManyField('Content', related_name='articles', blank=True)
#     quiz = models.ManyToManyField('Quiz', related_name='article_quizzes', blank=True)

#     def get_youtube_video_id(self, url):
#         parsed_url = urlparse(url)
#         if 'youtube.com' in parsed_url.netloc and 'v=' in parsed_url.query:
#             return parsed_url.query.split('v=')[1].split('&')[0]
#         elif 'youtu.be' in parsed_url.netloc:
#             return parsed_url.path.split('/')[1]
#         return None

#     def get_youtube_thumbnail_url(self, video_id):
#         return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"

#     def download_youtube_audio(self, article_video_url):
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'extractaudio': True,  # Download only audio
#             'audioformat': 'mp3',  # Save as mp3
#             'outtmpl': 'C:/Users/Admin/Desktop/wikitube/downloads/%(title)s.%(ext)s',  # Save to downloads folder
#             'timeout': 300,  # Increase timeout to 5 minutes
#             'noplaylist': True,  # Prevent downloading playlists
#         }

#         retries = 3
#         for attempt in range(retries):
#             try:
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     info_dict = ydl.extract_info(article_video_url, download=True)
#                     audio_file_path = ydl.prepare_filename(info_dict)
#                     print(f"Downloaded audio file to: {audio_file_path}")
#                     return audio_file_path
#             except Exception as e:
#                 if attempt < retries - 1:  # Don't raise on the last attempt
#                     print(f"Retrying download... Attempt {attempt + 2}/{retries}")
#                 else:
#                     raise Exception(f"Failed to download audio from YouTube: {str(e)}")

#     def upload_audio_to_s3(self, file_path, s3_file_name):
#         print(f"Uploading file from: {file_path}")
#         if not os.path.isfile(file_path):
#             raise FileNotFoundError(f"File not found at path: {file_path}")
#         s3 = boto3.client('s3',region_name=settings.AWS_S3_REGION_NAME)
#         retries = 3
#         for attempt in range(retries):
#             try:
#                 s3.upload_file(file_path, 'youtube-trans', s3_file_name)  # Upload to 'youtube-trans' bucket
#                 s3_url = f"https://youtube-trans.s3.amazonaws.com/{s3_file_name}"
#                 print(f"File uploaded successfully to: {s3_url}")
#                 return s3_url
#             except Exception as e:
#                 if attempt < retries - 1:  # Don't raise on the last attempt
#                     print(f"Retrying upload... Attempt {attempt + 2}/{retries}")
#                 else:
#                     raise Exception(f"Failed to upload file to S3: {str(e)}")
#     def start_transcription_job(self, s3_url, job_name):
#         transcribe = boto3.client('transcribe',region_name=settings.AWS_S3_REGION_NAME)

#         try:
#             transcribe.start_transcription_job(
#                 TranscriptionJobName=job_name,
#                 Media={'MediaFileUri': s3_url},
#                 MediaFormat='mp3',  # Ensure this matches the format of your uploaded audio
#                 LanguageCode='en-US'
#             )
#         except Exception as error:  # Change 'e' to 'error' here
#             raise Exception(f"Failed to start transcription job: {str(error)}")  # Use 'error' here


   
#     def get_transcription_result(self, job_name):
#         transcribe = boto3.client('transcribe',region_name='ap-south-1')
#         while True:
#             try:
#                 response = transcribe.get_transcription_job(TranscriptionJobName=job_name)
#                 status = response['TranscriptionJob']['TranscriptionJobStatus']
#                 if status == 'COMPLETED':
#                     transcript_url = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
#                     transcript_text = requests.get(transcript_url).json()['results']['transcripts'][0]['transcript']
#                     return transcript_text
#                 elif status in ['FAILED', 'CANCELLED']:
#                     raise Exception("Transcription job failed or was cancelled.")
#                 else:
#                     print("Transcription job is in progress...")
#                     time.sleep(10)  # Wait before polling again
#             except Exception as e:
#                 raise Exception(f"Failed to get transcription result: {str(e)}")

#     def cleanup_files(self, *files):
#         for file in files:
#             if os.path.isfile(file):
#                 os.remove(file)

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.article_name)

#         if self.article_video_url:
#             video_id = self.get_youtube_video_id(self.article_video_url)
#             if video_id:
#                 self.article_video_thumbnail = self.get_youtube_thumbnail_url(video_id)

#                 # Download and upload the audio
#                 audio_file = self.download_youtube_audio(self.article_video_url)
#                 s3_url = self.upload_audio_to_s3(audio_file, f'articles/{self.slug}.mp3')

#                 # Start transcription job
#                 job_name = f"transcription-{self.slug}"
#                 try:
#                     # Try to get the transcription job result if it already exists
#                     transcription_text = self.get_transcription_result(job_name)
#                     print(f"Transcription job already exists for {job_name}. Retrieved transcript.")
#                 except Exception as error:
#                     print(f"No existing transcription job found. Starting new job for {job_name}.")
#                     self.start_transcription_job(s3_url, job_name)

#                     # Fetch the transcription result (consider using a background task for production)
#                     transcription_text = self.get_transcription_result(job_name)
#                 # Save the transcript if available
#                 if transcription_text:
#                     self.transcript = transcription_text

#                 # Clean up local files
#                 self.cleanup_files(audio_file)

#         super(Article, self).save(*args, **kwargs)

#     def __str__(self):
#         return self.article_name

# #


class Hyperlink(models.Model):
    article = models.ForeignKey(Article, related_name='hyperlinks_set', blank=True, null=True,on_delete=models.CASCADE)
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
    content_name = models.CharField(max_length=255, unique=True)
    article = models.ForeignKey(Article, related_name='content', on_delete=models.CASCADE)

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
        return f"Quiz for {self.article.article_name}"


class UserPerformance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='course', null=True, on_delete=models.CASCADE)
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
