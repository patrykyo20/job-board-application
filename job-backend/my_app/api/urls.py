from django.urls import path
from .views import get_user, create_user, user_details, register, login, get_job, create_job, job_details
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('users/', get_user, name='get_user'),
  path('users/create/', create_user, name='create_user'),
  path('users/<int:pk>', user_details, name='user_details'),
  path('users/register/', register, name='register'),
  path('users/login/', login, name='login'),
  path('jobs/', get_job, name='get_job'),
  path('jobs/create/', create_job, name='create_job'),
  path('jobs/<int:pk>', job_details, name='job_details'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)