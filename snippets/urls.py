from django.urls import path, include
from rest_framework.routers import DefaultRouter

from snippets import views

# create a router and register our ViewSets with it
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')

# the api urls are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]