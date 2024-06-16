from django.urls import path
from api.views import LoginView, RegisterView, FriendRequest, FriendsList, UserSearch
urlpatterns = [
    path('v1/login/', LoginView.as_view()),
    path('v1/register/', RegisterView.as_view()),
    path('v1/friend-request/', FriendRequest.as_view(), name='friend-request'),
    path('v1/friend-request/<int:id>/', FriendRequest.as_view(), name='friend-request-detail'),
    path('v1/friends-list/', FriendsList.as_view(), name='friends-list'),
    path('v1/user-search/', UserSearch.as_view(), name='user-search'),
]