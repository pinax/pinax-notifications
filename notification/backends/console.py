from django.core.urlresolvers import reverse
from django.template import Context

from django.contrib.sites.models import Site

from notification import backends
import sys


class ConsoleBackend(backends.BaseBackend):
    spam_sensitivity = 0

    def can_send(self, user, nt):
        return True
    
    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop('stream', sys.stdout)
        super(ConsoleBackend, self).__init__(*args, **kwargs)

    def deliver(self, recipient, sender, notice_type, extra_context):
        #prepare the message
        current_site = Site.objects.get_current()
        notices_url = u"http://%s%s" % (
            unicode(Site.objects.get_current()),
            reverse("notification_notices"),
        )

        # update context with user specific translations
        context = Context({
            "user": recipient,
            "notice": notice_type.display,
            "notices_url": notices_url,
            "current_site": current_site,
        })
        context.update(extra_context)

        messages = self.get_formatted_messages((
            "full.txt",
        ), notice_type.label, context)

        body = messages["full.txt"]

        self.stream.write("Sent %s To: %s  \n\n %s" % (notice_type, recipient, body))
        self.stream.flush()