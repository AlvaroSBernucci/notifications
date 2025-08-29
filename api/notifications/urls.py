from rest_framework import routers
from . import views


router = routers.SimpleRouter(trailing_slash=False)
router.register("/api/notificacoes", views.NotificationView)