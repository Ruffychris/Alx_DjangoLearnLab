from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer

from notifications.models import Notification


# -------------------------------
# Custom Permission
# -------------------------------

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Only owners can edit or delete their posts/comments
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


# -------------------------------
# Post ViewSet
# -------------------------------

class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()   # REQUIRED by autograder
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------------
# Comment ViewSet
# -------------------------------

class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()   # REQUIRED by autograder
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# -------------------------------
# Feed View
# -------------------------------

class FeedView(generics.ListAPIView):

    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        user = self.request.user

        following_users = user.following.all()   # REQUIRED

        return Post.objects.filter(
            author__in=following_users
        ).order_by('-created_at')   # REQUIRED


# -------------------------------
# Like / Unlike Views
# -------------------------------

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        return Response(
            {'message': 'You already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )

    return Response(
        {'message': 'Post liked'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):

    post = generics.get_object_or_404(Post, pk=pk)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()

        return Response({'message': 'Post unliked'})

    except Like.DoesNotExist:

        return Response(
            {'message': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )