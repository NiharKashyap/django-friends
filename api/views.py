from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Friends
from .serializers import FriendRequestSerializer, RegisterSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .filters import UserFilter
import datetime
from django.utils import timezone


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class FriendRequest(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = request.user
        one_minute_ago = timezone.now() - datetime.timedelta(minutes=1)
        
        recent_requests_count = Friends.objects.filter(
            request_from=user,
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response({"detail": "You have reached the limit of 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        user = request.user
        received_requests = Friends.objects.filter(request_to=user, status=False)
        sent_requests = Friends.objects.filter(request_from=user, status=False)
        serializer_received = FriendRequestSerializer(received_requests, many=True)
        serializer_sent = FriendRequestSerializer(sent_requests, many=True)
        return Response({
            'received_requests': serializer_received.data,
            'sent_requests': serializer_sent.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, id):
        friend_request = get_object_or_404(Friends, id=id, request_to=request.user)
        if friend_request.status:
            return Response({"detail": "Request already accepted."}, status=status.HTTP_400_BAD_REQUEST)

        friend_request.status = True
        friend_request.save()
        return Response({"detail": "Friend request accepted."}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        friend_request = get_object_or_404(Friends, id=id, request_to=request.user)
        if friend_request.status:
            return Response({"detail": "Cannot delete an accepted friend request."}, status=status.HTTP_400_BAD_REQUEST)
        
        friend_request.delete()
        return Response({"detail": "Friend request deleted."}, status=status.HTTP_204_NO_CONTENT)
    
        

class FriendsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friends = Friends.objects.filter(
            status=True,
            request_from=user
        ).values_list('request_to', flat=True).union(
            Friends.objects.filter(
                status=True,
                request_to=user
            ).values_list('request_from', flat=True)
        )

        friends_list = User.objects.filter(id__in=friends)
        friends_data = [{'id': friend.id, 'username': friend.username} for friend in friends_list]

        return Response(friends_data, status=status.HTTP_200_OK)


class UserSearch(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        # Optionally add extra logic to the queryset if needed
        return queryset