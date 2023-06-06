from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name="index"),
    path('recepie/<int:id>', views.recepie, name="recepie"),
    path('user/dashboard', views.dashboard, name="dashboard")
]
