from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
 path('admin/', admin.site.urls),
    path('', views.index , name="index"),
    path('recepie/<slug:slug>', views.recepie, name="recepie"),
    path('user/dashboard', views.dashboard, name="dashboard"),
    path('user/dashboard/daydata', views.daydata, name="daydata"),
    path('user/dashboard/addnewday', views.create_day, name="createDAy"),
    path('user/dashboard/dayelement/<str:id>', views.setDayElementId, name="setDayElementId"),
    path('user/profile', views.user_profil, name="profile"),
    path('user/profile/changename', views.change_user_name, name="userName"),
    path('user/profile/changeemail', views.change_user_email, name="userEmail"),
    path('user/profile/changepassword', views.change_user_password, name="userPassword"),
    path('user/shoplist', views.shoplist, name="shoplist"),
    path('user/add/recepie', views.add_recepie, name="addrecepie"),
    path('user/addmealtoday/<int:id>/<str:slug>/<str:meal_type>', views.add_meal_to_day, name="addMealToDay"),
    path('user/deletemealfromday/<int:day_id>/<int:meal_id>', views.delete_meal_from_day, name= "deleteMealFromDay" ),
    path('user/deleteday/<int:day_id>', views.delete_day, name= "deleteDay" ),
    path('user/copyday/<int:day_id>', views.copy_day, name= "copyDay" ),
    path('user/copydish/<int:day_id>/<int:dish_id>/<str:element_id>', views.copy_dish, name= "copyDish" ),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('reset/', views.reset, name="reset"),
    path('reset/<str:token>', views.reset_password_view, name="resetPasswordView"),
    path('logout/', views.logout_view, name="logout"),
    path('message/', views.message, name="message"),
    path('activate/<str:token>', views.activate, name="activate"),
    path('change/email/<str:token>', views.activate_change_email, name="changeEmail"),
    path('activated/', views.user_activated, name="isActivated"),
    path('setidcookie/', views.set_user_id_cookie, name="setIdCookie"),
    path('getidcookie/', views.get_user_id_cookie, name="getIdCookie"),
    path('getproductsearch/<str:productname>', views.get_product_search, name="getProductSearch"),
    path('getrecepiesearch/<str:recepiename>', views.get_recepie_search, name="getRecepieSearch"),
    path('user/productslist/<str:days>', views.get_days_product_list, name="getDaysProductList")
]
