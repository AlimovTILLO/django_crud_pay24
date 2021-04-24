from django.conf.urls import include
from rest_framework import routers
from django.urls import path
from knox import views as knox_views
from django.contrib.auth.decorators import login_required

from .api import LoginAPI, CurrentUserView, PassportViewSet, AddPassportViewSet, PassportList


router = routers.DefaultRouter()
router.register('passports', PassportViewSet, 'passports')
router.register('addpassport', AddPassportViewSet, 'addpassport')

urlpatterns = [
    path("", include(router.urls), name='api'),
    # path('passports/', PassportList.as_view()),
    path("currentuser/", CurrentUserView.as_view(), name="currentuser"),
    path("login/", LoginAPI.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]