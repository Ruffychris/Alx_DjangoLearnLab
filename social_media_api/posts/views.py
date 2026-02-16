from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Comment
from accounts.models import User as CustomUser
from .serializers import PostSerializer, CommentSerializer

# ---------------------------
# Permissions
# ---------------------------
class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only owners to edit or delete objects."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

# ---------------------------
# Pagination
# ---------------------------
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ---------------------------
# Post ViewSet
# ---------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ---------------------------
# Comment ViewSet
# ---------------------------
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# ---------------------------
# Feed View
# ---------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def feed_view(request):
    # Get users the current user is following (explicit .all() call)
    following_users = request.user.following.all()

    # Fetch posts from followed users, newest first
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
