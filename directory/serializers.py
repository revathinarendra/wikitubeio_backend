from rest_framework import serializers
from .models import Article, Content, Course, Hyperlink, Quiz, VideoPlayer

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
from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
import re



class VideoPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoPlayer
        fields = ['video_played_id', 'video_title', 'video_description', 'channel_name']


class ArticleSerializer(serializers.ModelSerializer):
    hyperlinks = HyperlinkSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    content = ContentSerializer(many=True, read_only=True)
    videos = VideoPlayerSerializer(many=True, read_only=True)
    subtitles = serializers.SerializerMethodField()  # Add a field for subtitles

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
            'content',
            'videos',
            'subtitles', 
        ]

    def get_subtitles(self, obj):
        video_url = obj.article_video_url
        video_id = self.extract_video_id(video_url)

        if not video_id:
            return None

        try:
            # Fetch subtitles using youtube_transcript_api
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            return transcript
        except Exception as e:
            # If subtitles are not available or any error occurs
            print(f'Error fetching subtitles: {e}')
            return None

    def extract_video_id(self, url):
        # Regular expression to extract YouTube video ID
        video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        return video_id_match.group(1) if video_id_match else None



# class VideoPlayerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VideoPlayer
#         fields = [
#             'video_played_id',
#             'video_title',
#             'video_description',
#             'channel_name'
#         ]


# class ArticleSerializer(serializers.ModelSerializer):
#     hyperlinks = HyperlinkSerializer(many=True, read_only=True)
#     quizzes = QuizSerializer(many=True, read_only=True)
#     content = ContentSerializer(many=True, read_only=True)  # Add ContentSerializer here
#     videos = VideoPlayerSerializer(many=True, read_only=True)

#     class Meta:
#         model = Article
#         fields = [
#             'id', 
#             'course_name', 
#             'article_name', 
#             'slug', 
#             'description', 
#             'article_video_thumbnail', 
#             'article_video_url', 
#             'hyperlinks', 
#             'quizzes', 
#             'content' ,
#             'videos'
#         ]
        
