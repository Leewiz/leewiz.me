from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    this viewset automatically provides `list` and `retrieve` actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

class SnippetViewSet(viewsets.ModelViewSet):
    """
    this ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions
    """ 
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)