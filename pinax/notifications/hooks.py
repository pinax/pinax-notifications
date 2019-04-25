from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from .conf import settings
from .utils import load_media_defaults


class DefaultHookSet(object):

    def notice_setting_for_user(self, user, notice_type, medium, scoping=None):
        kwargs = {
            "notice_type": notice_type,
            "medium": medium
        }
        if scoping:
            kwargs.update({
                "scoping_content_type": ContentType.objects.get_for_model(scoping),
                "scoping_object_id": scoping.pk
            })
        else:
            kwargs.update({
                "scoping_content_type__isnull": True,
                "scoping_object_id__isnull": True
            })
        try:
            return user.noticesetting_set.get(**kwargs)
        except ObjectDoesNotExist:
            # _, NOTICE_MEDIA_DEFAULTS = load_media_defaults()
            if scoping is None:
                kwargs.pop("scoping_content_type__isnull")
                kwargs.pop("scoping_object_id__isnull")
                kwargs.update({
                    "scoping_content_type": None,
                    "scoping_object_id": None
                })
            default = False
            kwargs.update({"send": default, "user": user})
            from .models import NoticeSetting
            setting = NoticeSetting(**kwargs)
            return setting


class HookProxy(object):

    def __getattr__(self, attr):
        return getattr(settings.PINAX_NOTIFICATIONS_HOOKSET, attr)


hookset = HookProxy()
