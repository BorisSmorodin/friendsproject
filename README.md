# friendsproject
## Description
###### This is a simple friends API service project based on `Python` and `Django REST framework`
###### Operating principles are described in the documentation located in `/docs/API docs/index.html`
###### OpenApi specification can be found in `/docs/OpenApi specification.json`
## Dependencies
###### I used Python `version 3.10`, Django `version 4.1` and DRF `version 3.14.0`
## Runserver
###### It is necessary to make migrations before starting the app. Use `python manage.py migrate` or `python3 manage.py migrate` for it.
###### Application was tested on port 8001, so to follow the documentation use `python manage.py runserver 8001` or `python3 manage.py runserver 8001` to launch the app.
## Documentation
###### In the documentation you can find requests examples. 
## Models structure
###### `CustomUser` represents user. Has fields `id: int32`, `username: str` for username
###### `FriendRequest` represents friendship requests. Has fields `id: int32`, `from_user: FK to CustomUser` for user provided the request, `to_user: FK to Custom user` for user receiving the request, `status: int` for request status (0 - pending, 1 - accepted, 2 - rejected).
###### `Friends` represents friends pair. Has fields `id: int32`, `user_1: FK to CustomUser` for user provided the request, `user_2: FK to Custom user` for user accepted the request.
### Please be sure to register 3 or more users before following the documentation requests!
## Algorithm
###### `Registration` to create user records
###### `Send Friendship Request` to create friend request records
###### `Accept Friend Request` to accept or reject friendship reques or `mirored` (from_user = to_user, to_user = from_user) `Send friendship request` to accept friendship request. All acceptions will automaticly create friends record.
###### `Show Friend List` to check users friend list
###### `Show Requests Status` to check incomming and outgoing friendship request statuses
###### `Show User Requests` to check friendship status with any user
###### `Delete Friend` to delete Friends record and FriendRequest record
