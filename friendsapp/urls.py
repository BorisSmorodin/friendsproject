from django.urls import path
from .views import RegisterUserView, SendFriendRequestView, UpdateFriendRequestView, ListFriendRequestsView, \
    ListFriendsView, DeleteFriendView, GetStatusView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('send_request/', SendFriendRequestView.as_view(), name='send_request'),
    path('update_request/<int:pk>/', UpdateFriendRequestView.as_view(), name='update_request'),
    path('list_requests/', ListFriendRequestsView.as_view(), name='list_requests'),
    path('list_friends/', ListFriendsView.as_view(), name='list_friends'),
    path('delete_friend/<int:pk>/', DeleteFriendView.as_view(), name='delete_friend'),
    path('get_status/', GetStatusView.as_view(), name='get_status')
]
