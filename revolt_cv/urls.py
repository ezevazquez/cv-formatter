from django.contrib import admin
from django.urls import path
from cvapp.views import upload_cv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_cv, name='upload_cv'),
]
