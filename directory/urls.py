from django.urls import path
from .views import ArticleDetailView, CourseListView, QuizListView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('articles/<int:article_id>/quizzes/', QuizListView.as_view(), name='quiz-list'),
]
