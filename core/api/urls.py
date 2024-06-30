from django.urls import path, include
from home.views import index, person, login, PersonAPI, PersonViewSet, RegisterApi, LoginAPI
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'people', PersonViewSet, basename='people')
# urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('index/', index),
    path('person/', person),
    path('login/', login),
    path('person-api/', PersonAPI.as_view()),
]
