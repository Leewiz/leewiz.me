from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from snippets import views as snippet_views
from gtfs_rt import views as gtfs_rt_views

from debug_toolbar.toolbar import debug_toolbar_urls

router = routers.DefaultRouter()
router.register(r'users', snippet_views.UserViewSet)
router.register(r'snippets', snippet_views.SnippetViewSet)
router.register(r'subway-stations', gtfs_rt_views.SubwayStationViewSet, basename='subway-station')

app_name = "mysite"
urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gtfs-rt/subway', gtfs_rt_views.subway_form, name='subway'),
    path('gtfs-rt/subway/borough/stops', gtfs_rt_views.get_stops, name='get_stops'),
    path('gtfs-rt/subway/borough/stops/times', gtfs_rt_views.get_times_by_stop_id, name='get_times_by_stop_id'),
    path('gtfs-rt/data', gtfs_rt_views.get_train_data, name='get-train-data'),
    path('gtfs-rt/purge', gtfs_rt_views.purge_old_stop_data, name='purge-old-stop-data'),
    path('gtfs-rt/testview', gtfs_rt_views.SubwayStationViewSet.as_view({'get': 'list'}), name='testview'),
    path('api/', include(router.urls)),
    path('polls/', include('polls.urls')),
] + debug_toolbar_urls()