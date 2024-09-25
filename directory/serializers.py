from rest_framework import serializers
from .models import Article, Content, Course, Hyperlink, Quiz

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['course_id', 'course_name', 'slug']
from rest_framework import serializers
from .models import Course, UserPerformance


class UserPerformanceSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = UserPerformance
        fields = ['user', 'watched_videos', 'progress']

    def get_progress(self, obj):
        return obj.progress


# class CourseSerializer(serializers.ModelSerializer):
#     user_performance = serializers.SerializerMethodField()  # Custom field for nested performance

#     class Meta:
#         model = Course
#         fields = ['course_id', 'course_name', 'slug', 'total_videos', 'user_performance']

#     def get_user_performance(self, obj):
#         # Fetch user performance for the course
#         user = self.context.get('user')  # Expecting user in context
#         if user:
#             performance = UserPerformance.objects.filter(user=user, course=obj).first()
#             if performance:
#                 return UserPerformanceSerializer(performance).data
#         return None  # No performance found for the user

class CourseSerializer(serializers.ModelSerializer):
    user_performance = serializers.SerializerMethodField()  # Custom field for performance

    class Meta:
        model = Course
        fields = ['course_id', 'course_name', 'slug', 'total_videos', 'user_performance']

    def get_user_performance(self, obj):
        user = self.context.get('user')  # Expecting user in context
        if user:
            # Fetch user performance for the course
            performance = UserPerformance.objects.filter(user=user, course=obj).first()
            if performance:
                # If performance exists, calculate based on watched videos
                watched_videos_count = performance.watched_videos.count()
                total_videos_count = obj.total_videos  # Assuming you have a total_videos field
                progress = (watched_videos_count / total_videos_count) * 100 if total_videos_count > 0 else 0
                return {
                    "user": user.id,
                    "watched_videos": list(performance.watched_videos.values_list('id', flat=True)),
                    "progress": progress
                }
            else:
                # Return default progress of 50% if no performance data exists
                return {
                    "user": user.id,
                    "watched_videos": [],
                    "progress": 50  # Default progress is 50%
                }
        return None  # Return None if no user is in context

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
        
