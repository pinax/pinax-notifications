.. _settings:

Notification specific Settings
================================

The following allows you to specify the behavior of django-notification in your
project. Please be aware of the native Django settings which can affect the
behavior of django-notification.


NOTIFICATION_BACKENDS
---------------------

**Default**::
    
    [
        ("email", "notification.backends.email.EmailBackend"),
    ]

TODO: Describe usage. Look at Pinax


DEFAULT_HTTP_PROTOCOL
---------------------

**Default**: `http`

This is used to specify the beginning of URLs in the default `email_body.txt`
file. A common use-case for overriding this default might be `https` for use on
more secure projects.


NOTIFICATION_LANGUAGE_MODULE
----------------------------

**Default**: `Not defined`

The default behavior for this setting is that it does not exist. It allows users to specify their own notification language.

Example model in a `languages` app::

    from django.conf import settings

    class Language(models.Model):
    
        user = models.ForeignKey(User)
        language = models.CharField(_("language"), choices=settings.LANGUAGES, max_length="10")
        
Setting this value in `settings.py`::

    NOTIFICATION_LANGUAGE_MODULE = "languages.Language"


DEFAULT_FROM_EMAIL
------------------

**Default**: `webmaster@localhost`

Docs: https://docs.djangoproject.com/en/1.3/ref/settings/#default-from-email

Default e-mail address to use for various automated correspondence from 
notification.backends.email. Is actually part of Django core settings.


LANGUAGES
---------

**Default**: `A tuple of all available languages.`

Docs: https://docs.djangoproject.com/en/1.3/ref/settings/#languages

The default for this is specifically used for things like the Django admin.
However, if you need to specify a subset of languages for your site's front end
you can use this setting to override the default. In which case this is the
definated pattern of usage::

    gettext = lambda s: s

    LANGUAGES = (
        ('en', gettext('English')),
        ('fr', gettext('French')),
    )


NOTIFICATION_QUEUE_ALL
----------------------

**Default**: False

By default, calling `notification.send` will send the notification immediately,
however, if you set this setting to True, then the default behavior of the `send`
method will be to queue messages in the database for sending via the `emit_notices`
command.


NOTIFICATION_LOCK_WAIT_TIMEOUT
------------------------------

**Default**: -1

How long to wait for the lock to become available. Default of -1 means to never
wait for the lock to become available. This only applies when using crontab
setup to execute the `emit_notices` management command to send queued messages
rather than sending immediately.
