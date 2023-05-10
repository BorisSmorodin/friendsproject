from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=30)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, related_name='outgoing_request', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, related_name='incoming_request', on_delete=models.CASCADE)
    status = models.IntegerField(choices=((0, "Pending"), (1, "Accepted"), (2, "Rejected")), default=0)


class Friends(models.Model):
    user_1 = models.ForeignKey(CustomUser, related_name='friendsapp_Friends_user_1', on_delete=models.CASCADE)
    user_2 = models.ForeignKey(CustomUser, related_name='friendsapp_Friends_user_2', on_delete=models.CASCADE)