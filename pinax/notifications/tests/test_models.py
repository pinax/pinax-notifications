import base64

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.six.moves import cPickle as pickle

from . import get_backend_id
from ..conf import settings
from ..models import (
    LanguageStoreNotAvailable,
    NoticeQueueBatch,
    NoticeSetting,
    NoticeType,
    get_notification_language,
    queue,
    send,
    send_now,
)
from .models import Language


class BaseTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test_user", "test@user.com", "123456")
        self.user2 = get_user_model().objects.create_user("test_user2", "test2@user.com", "123456")
        NoticeType.create("label", "display", "description")
        self.notice_type = NoticeType.objects.get(label="label")

    def tearDown(self):
        self.user.delete()
        self.user2.delete()
        self.notice_type.delete()


class TestNoticeType(TestCase):

    def test_create(self):
        label = "friends_invite"
        NoticeType.create(label, "Invitation Received", "you received an invitation", default=2,
                          verbosity=2)
        n = NoticeType.objects.get(label=label)
        self.assertEqual(str(n), label)
        # update
        NoticeType.create(label, "Invitation for you", "you got an invitation", default=1,
                          verbosity=2)
        n = NoticeType.objects.get(pk=n.pk)
        self.assertEqual(n.display, "Invitation for you")
        self.assertEqual(n.description, "you got an invitation")
        self.assertEqual(n.default, 1)


class TestNoticeSetting(BaseTest):
    def test_for_user(self):
        email_id = get_backend_id("email")
        notice_setting = NoticeSetting.objects.create(
            user=self.user,
            notice_type=self.notice_type,
            medium=email_id,
            send=False
        )
        self.assertEqual(
            NoticeSetting.for_user(self.user, self.notice_type, email_id, scoping=None),
            notice_setting
        )

        # test default fallback
        NoticeSetting.objects.create(user=self.user2, notice_type=self.notice_type, medium=email_id, send=True, scoping=None)
        ns2 = NoticeSetting.objects.get(user=self.user2, notice_type=self.notice_type, medium=email_id)
        self.assertTrue(ns2.send)


class TestProcedures(BaseTest):
    def setUp(self):
        super(TestProcedures, self).setUp()
        self.lang = Language.objects.create(user=self.user, language="en_US")
        mail.outbox = []
        email_id = get_backend_id("email")
        NoticeSetting.objects.create(user=self.user, notice_type=self.notice_type, medium=email_id, send=True, scoping=None)
        NoticeSetting.objects.create(user=self.user2, notice_type=self.notice_type, medium=email_id, send=True, scoping=None)

    def tearDown(self):
        super(TestProcedures, self).tearDown()
        self.lang.delete()
        NoticeQueueBatch.objects.all().delete()

    @override_settings(PINAX_NOTIFICATIONS_LANGUAGE_MODEL="tests.Language")
    def test_get_notification_language(self):
        self.assertEqual(get_notification_language(self.user), "en_US")
        self.assertRaises(LanguageStoreNotAvailable, get_notification_language, self.user2)
        setattr(settings, "PINAX_NOTIFICATIONS_LANGUAGE_MODEL", None)
        self.assertRaises(LanguageStoreNotAvailable, get_notification_language, self.user)

    @override_settings(SITE_ID=1, PINAX_NOTIFICATIONS_LANGUAGE_MODEL="tests.Language")
    def test_send_now(self):
        Site.objects.create(domain="localhost", name="localhost")
        users = [self.user, self.user2]
        send_now(users, "label")
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn(self.user2.email, mail.outbox[1].to)

    @override_settings(SITE_ID=1)
    def test_send(self):
        self.assertRaises(AssertionError, send, queue=True, now=True)

        users = [self.user, self.user2]
        send(users, "label", now=True)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(self.user.email, mail.outbox[0].to)
        self.assertIn(self.user2.email, mail.outbox[1].to)

        send(users, "label", queue=True)
        self.assertEqual(NoticeQueueBatch.objects.count(), 1)
        batch = NoticeQueueBatch.objects.all()[0]
        notices = pickle.loads(base64.b64decode(batch.pickled_data))
        self.assertEqual(len(notices), 2)

    @override_settings(SITE_ID=1)
    def test_send_default(self):
        # default behaviout, send_now
        users = [self.user, self.user2]
        send(users, "label")
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(NoticeQueueBatch.objects.count(), 0)

    @override_settings(SITE_ID=1)
    def test_queue_queryset(self):
        users = get_user_model().objects.all()
        queue(users, "label")
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(NoticeQueueBatch.objects.count(), 1)
