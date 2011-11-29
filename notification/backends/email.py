from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext

from notification import backends


class EmailBackend(backends.BaseBackend):
    spam_sensitivity = 2
    
    def can_send(self, user, notice_type):
        can_send = super(EmailBackend, self).can_send(user, notice_type)
        if can_send and user.email:
            return True
        return False
        
    def deliver(self, recipient, sender, notice_type, extra_context):
        # TODO: require this to be passed in extra_context
        
        context = self.default_context()
        context.update({
            "recipient": recipient,
            "sender": sender,
            "notice": ugettext(notice_type.display),
        })
        context.update(extra_context)
        
        messages = self.get_formatted_messages((
            "short.txt",
            "full.txt"
        ), notice_type.label, context)
        
        subject = "".join(render_to_string("notification/email_subject.txt", {
            "message": messages["short.txt"],
        }, context).splitlines())
        
        body = render_to_string("notification/email_body.txt", {
            "message": messages["full.txt"],
        }, context)
        
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient.email])
