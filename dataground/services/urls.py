from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'services'

urlpatterns =[
    path('', views.index, name='index'),
    path('/profile/kakao/', views.profile, name='profile'),
    path('/profile/update', views.profile_update, name='profile_update'),
 ]