from django.urls import path

from .views import NoticeSettingsView

app_name = "pinax_notifications"

urlpatterns = [
    path("settings/", NoticeSettingsView.as_view(), name="notice_settings"),
]
