import pkg_resources
import django

if django.VERSION < (3, 2):
    default_app_config = "pinax.notifications.apps.AppConfig"
__version__ = pkg_resources.get_distribution("pinax-notifications").version
