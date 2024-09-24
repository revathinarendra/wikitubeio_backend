from rest_framework import serializers
from .models import Article, Content, Course, Hyperlink, Quiz

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'slug']

class HyperlinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hyperlink
        fields = ['hyper_link_word', 'hyper_link_word_url']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'article', 'question', 'options', 'opt_values', 'correct_options']

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['content_id','content_name']

class ArticleSerializer(serializers.ModelSerializer):
    hyperlinks = HyperlinkSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    content = ContentSerializer(many=True, read_only=True)  # Add ContentSerializer here

    class Meta:
        model = Article
        fields = [
            'id', 
            'course_name', 
            'article_name', 
            'slug', 
            'description', 
            'article_video_thumbnail', 
            'article_video_url', 
            'hyperlinks', 
            'quizzes', 
            'content' 
        ]
        
