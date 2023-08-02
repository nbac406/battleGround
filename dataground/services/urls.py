from django.urls import include, path, re_path
from . import views
from django.conf.urls.static import static
from config.settings import base

app_name = 'services'


urlpatterns =[
    path('', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('map_log/', views.match_log_map, name='map_log'),
    path('maps/', views.map_analysis, name='maps'),
    path('weapons/', views.weapon_analysis, name='weapons'),
    path('getMapImageURL', views.get_map_image_url, name='get_map_image_url'),
 ]

if base.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]