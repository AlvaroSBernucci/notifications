from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from notifications.views import NotificationView

router = routers.SimpleRouter(trailing_slash=False)
router.register("api/notificacoes", NotificationView, basename="notificacoes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]