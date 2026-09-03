from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from courses.api.serializers import SubjectSerializer, CourseSerializer, ContentSerializer, CourseWithContentsSrializer
from courses.models import Subject, Course
from django.db.models import Count
from .pagination import StandardPagination
from .permissions import IsEnrolled
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(
#         total_courses = Count('courses'),
#     )
#     pagination_class = StandardPagination
#     serializer_class = SubjectSerializer
    
# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(
#         total_courses = Count('courses'),
#     )
#     serializer_class = SubjectSerializer

class SubjectViewSet(ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(
        total_courses = Count('courses')
    )
    pagination_class = StandardPagination
    serializer_class = SubjectSerializer


class CourseViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    pagination_class = StandardPagination
    serializer_class = CourseSerializer
    
    @action(detail=True, methods=['post'], authentication_classes = [BasicAuthentication], permission_classes = [IsAuthenticated])
    def enroll(self, request, *args, **kwargs):
        course = self.get_object()
        course.students.add(self.request.user)
        return Response({'enrolled': True})
    @action(detail = True, methods= ['get'], serializer_class=CourseWithContentsSrializer, authentication_classes = [BasicAuthentication], permission_classes = [IsAuthenticated, IsEnrolled] )
    def contents(self, request, *args, **kwargs):
        return self.retrieve( request, *args, **kwargs)


    
    