from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from gtfs_rt import views

from debug_toolbar.toolbar import debug_toolbar_urls

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include('homepage.urls')),
    path('api/', include('snippets.urls')),
    path('polls/', include('polls.urls')),
    path('gtfs-rt/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + debug_toolbar_urls()