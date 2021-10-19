from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
  path('', views.image_upload, name='imageupload'),
  path('login/', views.Login.as_view(), name='login'),
  path('logupt/', views.Logout.as_view(), name='logout'),
  path('signup/', views.SignUp.as_view(), name='signup'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
