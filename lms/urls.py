from django.urls import path
from rest_framework.routers import DefaultRouter

from lms import views
from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonCreateAPIView, LessonDestroyAPIView, LessonListAPIView,
                       LessonRetrieveAPIView, LessonUpdateAPIView)

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson"),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path("lesson/delete/<int:pk>/", LessonDestroyAPIView.as_view(), name="lesson_delete"),
                  path(
                      'courses/<int:course_id>/toggle-subscription/',
                      views.ToggleCourseSubscriptionView.as_view(),
                      name='toggle-subscription'),
] + router.urls
