from django.conf import settings

from django.urls import path

from authenticator.views import LoginUser, RegisterUser

urlpatterns = [
    path('signin/', LoginUser.as_view(), name='signin'),
    path('signup/', RegisterUser.as_view(), name='signup'),
]
