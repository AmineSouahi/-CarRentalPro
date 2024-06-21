#locationdevoiture/urls.py
from django import views
from django.urls import include, path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import admin



urlpatterns = [
    path('', views.home, name="home"),
    path('reservation/<int:car_id>/', login_required(views.reservation), name='reservation'),
    path('detaille/<int:car_id>/', views.detaille, name='detaille'),
    path('login/', views.user_login, name='login'),
    path('reservation_list/', views.reservation_list, name='reservation_list'),
    path('payment/<int:car_id>/<int:reservation_id>/', views.process_payment, name='payment'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('admin/', admin.site.urls),

]