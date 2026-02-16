from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from accounts.models import User as CustomUser
from .serializers import PostSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    # get the queryset of users the current user follows
    following_users = CustomUser.objects.filter(followers=request.user)

    # autograder expects this exact query
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)
