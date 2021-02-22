from django.urls import path
from django.conf.urls import url
from django.conf import settings
# from backend.djangoapps.main.views import UserView
from .views import UserView, SignView

# from ba.views import MeetingView as MeetingView
urlpatterns = [

    url(r'^v1/user$', UserView.as_view()),
    url(r'^v1/sign$', SignView.as_view()),

]
