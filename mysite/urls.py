from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from snippets import views as snippet_views
from gtfs_rt import views as gtfs_rt_views

from debug_toolbar.toolbar import debug_toolbar_urls

router = routers.DefaultRouter()
router.register(r'users', snippet_views.UserViewSet)
router.register(r'snippets', snippet_views.SnippetViewSet)

urlpatterns = [
    path('', include('homepage.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gtfs-rt/', gtfs_rt_views.get_train_data, name='get-train-data'),
    path('gtfs-rt/', gtfs_rt_views.hello_world, name='hello-world-api'),
    path('api/', include(router.urls)),
    path('polls/', include('polls.urls')),
] + debug_toolbar_urls()