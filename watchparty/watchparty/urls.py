from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from watchpartyapi.views import register_user, login_user
from watchpartyapi.views import SportTypes
from watchpartyapi.views import Games
from watchpartyapi.views import Fans
from watchpartyapi.views import WatchParties

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'sporttypes', SportTypes, 'sporttype')
router.register(r'games', Games, 'game')
router.register(r'fans', Fans, 'fan')
router.register(r'watchparties', WatchParties, 'watchparty')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
