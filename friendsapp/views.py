from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser, FriendRequest, Friends
from .serializers import UserSerializer, FriendRequestSerializer, FriendsSerializer
from enum import Enum
from rest_framework import status


def cross_request_status_update(from_user: int, to_user: int) -> None:
    """
    This function takes user ids as input and changes the status of request to "accepted; returns None"
    """
    FriendRequest.objects.filter(from_user=to_user, to_user=from_user).update(status=1)


def add_to_friends(from_user: int, to_user: int) -> None:
    """
    This function takes user ids as input and creates new obj in Friends table if the similar obj have not been found
    """
    if not Friends.objects.filter(user_1=from_user, user_2=to_user):
        if not Friends.objects.filter(user_1=to_user, user_2=from_user):
            user_1 = CustomUser.objects.filter(id=from_user).first()
            user_2 = CustomUser.objects.filter(id=to_user).first()
            friends_object = Friends()
            friends_object.user_1 = user_1
            friends_object.user_2 = user_2
            friends_object.save()


def on_delete_update(from_user: int, to_user: int) -> None:
    """
    This function takes user ids as input and deletes the request object from table just like in cascade delete method.
    """
    queryset = FriendRequest.objects.all()
    inst = queryset.filter(from_user=from_user, to_user=to_user)
    if inst.first():
        inst.delete()
    else:
        inst = queryset.filter(from_user=to_user, to_user=from_user)
        if inst.first():
            inst.delete()


def is_registered_user(user_id: int):
    """Function that takes user id as input and checks if it in th User table"""
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except:
            pass
    return user_id in [user.id for user in CustomUser.objects.all()]


def validate_user_id(user_id):
    if not type(user_id) == int:
        try:
            return int(user_id)
        except ValueError:
            return user_id


class EnumRequestStatus(Enum):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2


class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class SendFriendRequestView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        from_user: int = request.data['from_user']
        to_user: int = request.data['to_user']
        if not (is_registered_user(from_user) and is_registered_user(to_user)):
            response = {"message": f"One or both users have not been found"}
            return Response(data=response, status=404)
        if self.queryset.filter(from_user=from_user, to_user=to_user).first():
            response = {"message": "Forbidden. Friend request is already exists"}
            return Response(data=response, status=status.HTTP_403_FORBIDDEN)
        request_cross = self.queryset.filter(from_user=to_user, to_user=from_user).first()
        if request_cross:
            if self.queryset.filter(from_user=from_user, to_user=to_user).first():
                response = {"message": "Forbidden. Friend request is already exists"}
                return Response(data=response, status=status.HTTP_403_FORBIDDEN)
            self.cross_request_add_to_friends(to_user, from_user)
            response = {"id": request_cross.id,
                        "status": 1,
                        "from_user": request_cross.from_user.id,
                        "to_user": request_cross.to_user.id}
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return super().post(request, *args, **kwargs)

    @staticmethod
    def cross_request_add_to_friends(from_user, to_user):
        cross_request_status_update(to_user, from_user)
        add_to_friends(to_user, from_user)


class UpdateFriendRequestView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = []

    def put(self, request, *args, **kwargs):
        to_user = request.data['to_user']
        from_user = request.data['from_user']
        if not (is_registered_user(from_user) and is_registered_user(to_user)):
            response = {"message": f"One or both users have not been found"}
            return Response(data=response, status=404)
        request_obj = self.queryset.get(id=kwargs['pk'])
        if request_obj.from_user == CustomUser.objects.get(
                id=request.data['from_user']) and request_obj.to_user == CustomUser.objects.get(
            id=request.data['to_user']):
            if request_obj.status == EnumRequestStatus.PENDING.value:
                add_to_friends(request.data['from_user'], to_user)
                return super().put(request, *args, **kwargs)
            else:
                response = {"message": "Forbidden action"}
                return Response(data=response, status=403)
        else:
            response = {"message": "Forbidden action"}
            return Response(data=response, status=403)


class ListFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get(self, request, *args, **kwargs):
        user_id: int = request.query_params.get('id', None)
        if user_id:
            if not is_registered_user(user_id):
                response = {"message": f"No user with id={user_id} have been found"}
                return Response(data=response, status=404)
            queryset_from = self.queryset.filter(from_user=user_id).exclude(status=2).exclude(status=1)
            queryset_to = self.queryset.filter(to_user=user_id).exclude(status=2).exclude(status=1)
            response = {
                "Incoming requests": self.queryset_to_list(queryset_to, True),
                "Outgoing requests": self.queryset_to_list(queryset_from, False)
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {"message": "Bad request. User id was not provided"}
            return Response(data=response, status=400)

    @staticmethod
    def queryset_to_list(queryset, incoming: bool) -> list:
        if incoming:
            return [{'user_id': it.from_user.id} for it in queryset]
        else:
            return [{'user_id': it.to_user.id} for it in queryset]


class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendsSerializer
    queryset = Friends.objects.all()

    def get(self, request, *args, **kwargs):
        user_id: int = request.query_params.get('id', None)
        if not is_registered_user(user_id):
            response = {"message": f"No user with id={user_id} have been found"}
            return Response(data=response, status=404)
        if user_id:
            primary_queryset = self.queryset.filter(user_1=user_id)
            additional_queryset = self.queryset.filter(user_2=user_id)
            friends = [it.user_2.id for it in primary_queryset]
            friends.extend([it.user_1.id for it in additional_queryset])
            response = {'Friends_list': friends}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message": "Bad request. User id was not provided"}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class GetStatusView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    @staticmethod
    def status_to_string(status: int) -> str:
        match status:
            case 0:
                return EnumRequestStatus.PENDING.name
            case 1:
                return EnumRequestStatus.ACCEPTED.name
            case 2:
                return EnumRequestStatus.REJECTED.name

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', None)
        target_id = request.query_params.get('target_id', None)
        if user_id and target_id:
            if not (is_registered_user(user_id) and is_registered_user(target_id)):
                response = {"message": f"One or both users have not been found"}
                return Response(data=response, status=404)
            user_main = CustomUser.objects.get(id=user_id)
            user_target = CustomUser.objects.get(id=target_id)
            request_status_from = self.queryset.filter(from_user=user_main, to_user=user_target)
            if request_status_from:
                response = {
                    "message": f"Outgoing request. Status: {self.status_to_string(request_status_from.first().status)}"}
                return Response(
                    data=response, status=status.HTTP_200_OK)
            request_status_to = self.queryset.filter(from_user=user_target, to_user=user_main)
            if request_status_to:
                response = {
                    "message": f"Incoming request. Status: {self.status_to_string(request_status_to.first().status)}"}
                return Response(data=response, status=status.HTTP_200_OK)
            response = {"message": "No information have been found"}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {"message": "Bad request. User ids were not provided"}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class DeleteFriendView(generics.DestroyAPIView):
    serializer_class = FriendsSerializer
    queryset = Friends.objects.all()

    def delete(self, request, *args, **kwargs):
        if not (is_registered_user(request.data['user_1']) and is_registered_user(request.data['user_2'])):
            return Response(data={"message": f"One or both users have not been found"}, status=404)
        user_1 = CustomUser.objects.get(id=request.data['user_1'])
        user_2 = CustomUser.objects.get(id=request.data['user_2'])
        on_delete_update(user_1, user_2)
        return super().delete(request, *args, **kwargs)
