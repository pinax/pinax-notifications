import sys

from django.conf import settings
from django.core import exceptions

from .base import BaseBackend


# pylint: disable-msg=C0103
# mostly for backend compatibility
default_backends = [
    ("email", "notification.backends.email.EmailBackend"),
]


def load_backends():
    backends = []
    configured_backends = getattr(settings, "NOTIFICATION_BACKENDS", default_backends)
    for medium_id, bits in enumerate(configured_backends):
        if len(bits) == 2:
            label, backend_path = bits
            spam_sensitivity = None
        elif len(bits) == 3:
            label, backend_path, spam_sensitivity = bits
        else:
            raise exceptions.ImproperlyConfigured(
                "NOTIFICATION_BACKENDS does not contain enough data."
            )
        dot = backend_path.rindex(".")
        backend_mod, backend_class = backend_path[:dot], backend_path[dot + 1:]
        try:
            # import the module and get the module from sys.modules
            __import__(backend_mod)
            mod = sys.modules[backend_mod]
        except ImportError as e:
            raise exceptions.ImproperlyConfigured(
                "Error importing notification backend {}: \"{}\"".format(backend_mod, e)
            )
        # add the backend label and an instantiated backend class to the
        # backends list.
        backend_instance = getattr(mod, backend_class)(medium_id, spam_sensitivity)
        backends.append(((medium_id, label), backend_instance))
    return dict(backends)


def load_media_defaults(backends):
    media = []
    defaults = {}
    for key, backend in backends.items():
        # key is a tuple (medium_id, backend_label)
        media.append(key)
        defaults[key[0]] = backend.spam_sensitivity
    return media, defaults
