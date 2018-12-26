"""flightapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from portfolio.api.views import FastPaceUserSignup, FastPaceUserLogin, FastPaceUserViewSet
from flight.api.views import FlightViewSet, TicketViewSet

router = DefaultRouter()
router.register(r'user', FastPaceUserViewSet, base_name='users')
router.register(r'ticket', TicketViewSet, base_name='tickets')
router.register(r'flight', FlightViewSet, base_name='flights')

api_v1 = [
    url(r'^', include(router.urls)),
    url(r'^signup/$', FastPaceUserSignup.as_view(), name="sign_up"),
    url(r'^login/$', FastPaceUserLogin.as_view(), name="login"),
    url(r'^api-auth/', include('rest_framework.urls')),
]

urlpatterns = [
    url(r'^api/v1/', include(api_v1)),
    url(r'^admin/', admin.site.urls),
]
