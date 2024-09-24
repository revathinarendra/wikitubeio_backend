from rest_framework import generics
from .models import Course
from .serializers import CourseSerializer

# API View to get the list of courses
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
