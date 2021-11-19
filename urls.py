import rest_framework.request
from django.urls import include, path
from rest_framework import routers
from mirumee_webapp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'cores', views.RocketCoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('choose-favorite/', views.choose_favorite_rocket_core),
    path('view-favorite/', views.view_favorite_rocket)

]
