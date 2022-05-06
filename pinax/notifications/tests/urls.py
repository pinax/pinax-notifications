from django.urls import include, path

urlpatterns = [
    path("notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
]
