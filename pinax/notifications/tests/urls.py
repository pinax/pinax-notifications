from django.urls import include, re_path

urlpatterns = [
    re_path(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
]
