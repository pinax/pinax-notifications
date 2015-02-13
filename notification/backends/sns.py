from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from boto import connect_sns
from json import dumps
from django.conf import settings

from notification import backends


class SnsBackend(backends.BaseBackend):
    """ Uses AWS SNS for flushing the notification
    """
    spam_sensitivity = 2

    def __init__(self, medium_id, spam_sensitivity=None):
        aws_key = settings.NOTIFICATION_AWS_KEY
        aws_secret = settings.NOTIFICATION_AWS_SECRET
    
        self.sns = connect_sns(aws_key,
                               aws_secret)
        super(SnsBackend, self).__init__(medium_id, spam_sensitivity)

    def can_send(self, user, notice_type):
        can_send = super(SnsBackend, self).can_send(user, notice_type)
        return True
    
    def get_or_create_topic(self, notice_type):
        topic = 'DN-%s' % notice_type.upper()
        tpc_resp = self.sns.get_all_topics()
        if isinstance(tpc_resp, dict) \
                and 'ListTopicsResponse' in tpc_resp:
            topics = tpc_resp['ListTopicsResponse'] \
                ['ListTopicsResult']['Topics']
            print topics
            cur_tpc = [ kv['TopicArn'] for kv in topics]
            for tpc in cur_tpc:
                if tpc.endswith(topic):
                    return tpc

        ctpc_resp = self.sns.create_topic(topic)
        if isinstance(ctpc_resp, dict) \
                and 'CreateTopicResponse' in tpc_resp:
            topic = ctpc_resp['CreateTopicResponse'] \
                ['CreateTopicResult']['TopicArn']
            return topic
        
    def deliver(self, recipient, sender, notice_type, extra_context):
      
        context = self.default_context()
        context['current_site'] = context['current_site'].domain
        context.update({
            "recipient": recipient.get_absolute_url(),
            "sender": sender,
            "notice": ugettext(notice_type.label),
        })
        context.update(extra_context)
        topic = self.get_or_create_topic(notice_type.label)
        self.sns.publish(topic, context, notice_type.label)
        
