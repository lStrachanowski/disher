from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
 path('admin/', admin.site.urls),
    path('', views.index , name="index"),
    path('recepie/<slug:slug>', views.recepie, name="recepie"),
    path('user/dashboard', views.dashboard, name="dashboard"),
    path('user/dashboard/daydata', views.daydata, name="daydata"),
    path('user/profile', views.user_profil, name="profile"),
    path('user/shoplist', views.shoplist, name="shoplist"),
    path('user/add/recepie', views.add_recepie, name="addrecepie"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('reset/<str:token>', views.reset_password_view, name="resetPasswordView"),
    path('logout/', views.logout_view, name="logout"),
    path('success/', views.success, name="success"),
    path('activate/<str:token>', views.activate, name="activate"),
    path('activated/', views.user_activated, name="isActivated")
]
