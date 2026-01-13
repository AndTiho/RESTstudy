from lms.apps import LmsConfig
from rest_framework.routers import  DefaultRouter

from lms.views import CourseViewSet

app_name = LmsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns =[

] + router.urls