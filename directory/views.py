from rest_framework import generics
from .models import Article, Course, Quiz
from .serializers import ArticleSerializer, CourseSerializer, QuizSerializer

# API View to get the list of courses
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
# API View to get the list of articles
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
# API View to get details of a specific article based on the slug
class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'  
# API View for questions related to article
class QuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        article_id = self.kwargs['article_id']  # Get article ID from URL
        return Quiz.objects.filter(article_name_id=article_id)  # Filter questions by article ID