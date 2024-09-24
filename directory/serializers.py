from rest_framework import serializers
from .models import Article, Course, Hyperlink, Quiz

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'slug']
class HyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hyperlink
        fields = ['hyper_link_word', 'hyper_link_word_url']

class ArticleSerializer(serializers.ModelSerializer):
    article_video_thumbnail = serializers.ImageField(use_url=True) 
    hyperlinks = HyperlinkSerializer(many=True, read_only=True)


    class Meta:
        model = Article
        fields = ['id', 'course_name', 'article_name', 'slug', 'description', 'article_video_thumbnail', 'article_video_url','hyperlinks']
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'article_name', 'question', 'options', 'opt_values', 'correct_options']