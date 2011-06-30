from django.core.cache import cache
from django.contrib.auth.models import User
from django.test import TestCase

from notification.models import NoticeType, NoticeSetting

class BaseTest(TestCase):
    
    def setUp(self):
        
        self.user = User.objects.create_user('testuser','test@example.com','pw')
        self.user.save()


class TestNoticeType(BaseTest):

    def test_create(self):
        
        self.assertEquals(NoticeType.objects.count(), 0)
        NoticeType.create("notice_type", "New notice type", "You have a new notice type")
        self.assertEquals(NoticeType.objects.count(), 1)