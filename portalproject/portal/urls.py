

# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, home, calc, enrollment_view, loginUser, logoutUser, registerUser

router = DefaultRouter()
router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', loginUser, name='login'),
    path('register/', registerUser, name='register'),
    path('logout', logoutUser, name='logout'),
    path('home/', home, name='home'),
    path('calc/<str:level>', calc, name='calc'),
    path('enrollment/<int:level>', enrollment_view, name='enrollment_view'),
    path(
        'api/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='api'),
]
