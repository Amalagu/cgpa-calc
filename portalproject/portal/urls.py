

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, home

router = DefaultRouter()
router.register(r'courses', CourseViewSet)



urlpatterns = [path('', include(router.urls)),  path('', home, name='home' ), path('api/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='api' ),]