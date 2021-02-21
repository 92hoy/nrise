from django.urls import path
from django.conf.urls import url
from django.conf import settings
from backend.djangoapps.main.views import UserView

# from ba.views import MeetingView as MeetingView
urlpatterns = [
    url(r'^v1/user$', UserView.as_view()),
    # path("v1/user", UserView.as_view({"post": "create", "put": "update", "delete": "delete", "get": "read"}),
    #      name="user"),
    # path("v1/music/<int:music_num>", UserViewSet.as_view({"get": "list"}), name="music"),
]
