![](http://pinaxproject.com/pinax-design/patches/pinax-notifications.svg)

# Pinax Notifications

[![](https://img.shields.io/pypi/v/pinax-notifications.svg)](https://pypi.python.org/pypi/pinax-notifications/)

[![CircleCi](https://img.shields.io/circleci/project/github/pinax/pinax-notifications.svg)](https://circleci.com/gh/pinax/pinax-notifications)
[![Codecov](https://img.shields.io/codecov/c/github/pinax/pinax-notifications.svg)](https://codecov.io/gh/pinax/pinax-notifications)
[![](https://img.shields.io/github/contributors/pinax/pinax-notifications.svg)](https://github.com/pinax/pinax-notifications/graphs/contributors)
[![](https://img.shields.io/github/issues-pr/pinax/pinax-notifications.svg)](https://github.com/pinax/pinax-notifications/pulls)
[![](https://img.shields.io/github/issues-pr-closed/pinax/pinax-notifications.svg)](https://github.com/pinax/pinax-notifications/pulls?q=is%3Apr+is%3Aclosed)

[![](http://slack.pinaxproject.com/badge.svg)](http://slack.pinaxproject.com/)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)


## Table of Contents

* [About Pinax](#about-pinax)
* [Important Links](#important-links)
* [Overview](#overview)
  * [Features](#features)
  * [Supported Django and Python Versions](#supported-django-and-python-versions)
* [Documentation](#documentation)
  * [Installation](#installation)
  * [Usage](#usage)
    * [Creating Notice Types](#creating-notice-types)
    * [Templates](#templates)
    * [Backend Templates](#backend-templates)
  * [Settings](#settings)
  * [Scoping Notifications](#scoping-notifications)
* [Change Log](#change-log)
* [History](#history)
* [Contribute](#contribute)
* [Code of Conduct](#code-of-conduct)
* [Connect with Pinax](#connect-with-pinax)
* [License](#license)


## About Pinax

Pinax is an open-source platform built on the Django Web Framework. It is an ecosystem of reusable Django apps, themes, and starter project templates. This collection can be found at http://pinaxproject.com.


## Important Links

Where you can find what you need:
* Releases: published to [PyPI](https://pypi.org/search/?q=pinax) or tagged in app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Global documentation: [Pinax documentation website](https://pinaxproject.com/pinax/)
* App specific documentation: app repos in the [Pinax GitHub organization](https://github.com/pinax/)
* Support information: [SUPPORT.md](https://github.com/pinax/.github/blob/master/SUPPORT.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Contributing information: [CONTRIBUTING.md](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) file in the [Pinax default community health file repo](https://github.com/pinax/.github/)
* Current and historical release docs: [Pinax Wiki](https://github.com/pinax/pinax/wiki/)


## pinax-notifications

### Overview

`pinax-notifications` is a user notification management app for the Django web framework. 
Many sites need to notify users when certain events have occurred and to allow
configurable options as to how those notifications are to be received. `pinax-notifications` serves this need.

#### Features

* Submission of notification messages by other apps
* Notification messages via email (configurable by user)
* Ability to supply your own backend notification channels
* Ability to scope notifications at the site level

#### Supported Django and Python Versions

Django / Python | 3.6 | 3.7 | 3.8
--------------- | --- | --- | ---
2.2  |  *  |  *  |  *
3.0  |  *  |  *  |  *


## Documentation

### Installation

To install pinax-notifications:

```shell
$ pip install pinax-notifications
```

Add `pinax.notifications` to your `INSTALLED_APPS` setting:

```python
INSTALLED_APPS = [
    # other apps
    "pinax.notifications",
]
```

Add `pinax.notifications.urls` to your project urlpatterns:

```python
urlpatterns = [
    # other urls
    url(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
]
```

### Usage

Integrating notification support into your app is a three-step process:

1. create your notice types
1. create your notice templates
1. send notifications

#### Creating Notice Types

You need to call `NoticeType.create(label, display, description)` once to
create the notice types for your application in the database.
 
* `label` is the internal shortname that will be used for the type
* `display` is what the user sees as the name of the notification type
* `description` is a short description

For example:

```python
from pinax.notifications.models import NoticeType

NoticeType.create(
    "friends_invite",
    "Invitation Received",
    "you have received an invitation"
)
```

One way to create notice types is using a custom `AppConfig`. Here is an example:

```python
# myapp/signals/handlers.py

from django.conf import settings
from django.utils.translation import gettext_noop as _

def create_notice_types(sender, **kwargs): 
    if "pinax.notifications" in settings.INSTALLED_APPS:
        from pinax.notifications.models import NoticeType
        print("Creating notices for myapp")
        NoticeType.create("friends_invite", _("Invitation Received"), _("you have received an invitation"))
        NoticeType.create("friends_accept", _("Acceptance Received"), _("an invitation you sent has been accepted"))
    else:
        print("Skipping creation of NoticeTypes as notification app not found")
```

Notice that the code is wrapped in a conditional clause so if
`pinax-notifications` is not installed, your app will proceed anyway.

Note that the display and description arguments are marked for translation by
using gettext_noop. That will enable you to use Django's makemessages
management command and use `pinax-notifications` i18n capabilities.

```python
# myapp/apps.py

from django.apps import AppConfig
from django.db.models.signals import post_migrate

from myapp.signals import handlers

class MyAppConfig(AppConfig):
    name = 'myapp'
    verbose_name = 'My App'

    def ready(self):
        post_migrate.connect(handlers.create_notice_types, sender=self)
```

This will call the handler to create notices after the application is migrated.

```python
# myapp/__init__.py

default_app_config = 'myapp.apps.MyAppConfig'
```

#### Templates

Default templates are provided by the `pinax-templates` app in the
[notifications](https://github.com/pinax/pinax-templates/tree/master/pinax/templates/templates/pinax/notifications)
section of that project.

Reference pinax-templates
[installation instructions](https://github.com/pinax/pinax-templates/blob/master/README.md#installation)
to include these templates in your project.

View live `pinax-templates` examples and source at [Pinax Templates](https://templates.pinaxproject.com/notifications/settings/)!

##### Customizing Templates

Override the default `pinax-templates` templates by copying them into your project
subdirectory `pinax/notifications/` on the template path and modifying as needed.

For example if your project doesn't use Bootstrap, copy the desired templates
then remove Bootstrap and Font Awesome class names from your copies.
Remove class references like `class="btn btn-success"` and `class="icon icon-pencil"` as well as
`bootstrap` from the `{% load i18n bootstrap %}` statement.
Since `bootstrap` template tags and filters are no longer loaded, you'll also need to update
`{{ form|bootstrap }}` to `{{ form }}` since the "bootstrap" filter is no longer available.

##### `base.html`

Base template for other templates.

##### `notice_settings.html`

This template allows the user to specify which notices they want to receive.
This template is rendered by the sole view in `pinax.notifications.views` with the context
containing a list of available `notice_types` as well as the `request.user`'s settings
for those notice types.

#### Backend Templates

Four templates included with `pinax-templates` support the
single email backend that is included with `pinax-notifications`.

##### `short.txt`
 
Renders to the email subject.

##### `full.txt`
 
Renders to the email body.

##### `email_body.txt`

Renders the entire email body. Contains `full.txt`.

##### `email_subject.txt`

Renders the entire email subject. Contains `short.txt`.

In addition to the extra context supplied via the `send` call in your
site or app, these templates are rendered with the following context variables:

* `default_http_protocol` - `https` if `settings.PINAX_USE_SSL` is True, otherwise `http`
* `current_site` - `Site.objects.get_current()`
* `base_url` - the default http protocol combined with the current site domain
* `recipient` - the user who is getting the notice
* `sender` - the value supplied to the `sender` kwarg of the `send` method (often this is not set and will be `None`)
* `notice` - display value of the notice type

You can override default templates shipped with `pinax-templates` by adding alternative templates
to a directory on the template path called `pinax/notifications/<notice_type_label>/`.
For the example NoticeType above we might override `short.txt` to surround the notice with asterisks:

```django
{# pinax/notifications/friends_invite/short.txt #}
{% autoescape off %}{% load i18n %}{% blocktrans %}*** {{ notice }} ***{% endblocktrans %}{% endautoescape %}
```

If any of the four email backend templates are missing from the alternative directory,
the appropriate installed default template is used.

#### Sending Notifications

There are two different ways of sending out notifications. We have support
for blocking and non-blocking methods of sending notifications. The most
simple way to send out a notification, for example::

```python
from pinax.notifications.models import send_now, send, queue

send([to_user], "friends_invite", {"from_user": from_user})
```

One thing to note is that `send` is a proxy around either `send_now` or
`queue`. They all have the same signature::

```python
send(users, label, extra_context)
```

The parameters are:

* `users` is an iterable of `User` objects to send the notification to.
* `label` is the label you used in the previous step to identify the notice type.
* `extra_content` is a dictionary to add custom context entries to the template
   used to render to notification. This is optional.

##### `send_now` vs. `queue` vs. `send`

Lets first break down what each does.

###### `send_now`

This is a blocking call that will check each user for elgibility of the
notice and actually peform the send.

###### `queue`

This is a non-blocking call that will queue the call to `send_now` to
be executed at a later time. To later execute the call you need to use
the `emit_notices` management command.

###### `send`

A proxy around `send_now` and `queue`. It gets its behavior from a global
setting named `PINAX_NOTIFICATIONS_QUEUE_ALL`. By default it is `False`. This
setting is meant to help control whether you want to queue any call to `send`.

`send` also accepts `now` and `queue` keyword arguments. By default each option
is set to `False` to honor the global setting which is `False`. This enables
you to override on a per call basis whether it should call `send_now` or
`queue`.

#### Optional Notification Support

In case you want to use `pinax-notifications` in your reusable app, you can wrap
the import of `pinax-notifications` in a conditional clause that tests if it's
installed before sending a notice. As a result your app or project still
functions without notification.

For example:

```python
from django.conf import settings

if "notification" in settings.INSTALLED_APPS:
    from pinax.notifications import models as notification
else:
    notification = None
```

and then, later:

```python
if notification:
    notification.send([to_user], "friends_invite", {"from_user": from_user})
```

### Settings

The following allows you to specify the behavior of `pinax-notifications` in
your project. Please be aware of the native Django settings which can affect
the behavior of `pinax-notifications`.

#### PINAX_NOTIFICATIONS_BACKENDS

Defaults to:

```python
[
    ("email", "pinax.notifications.backends.email.EmailBackend"),
]
```

Formerly named `NOTIFICATION_BACKENDS`.

#### PINAX_USE_SSL

_This is a proposed common setting across the Pinax ecosystem. It currently may
not be consistant across all apps._

Defaults to `False`.

This is used to specify the beginning of URLs in the default `email_body.txt`
file. A common use-case for overriding this default might be `https` for use on
more secure projects.

Formerly named `DEFAULT_HTTP_PROTOCOL` and defaulted to "http".

#### PINAX_NOTIFICATIONS_LANGUAGE_MODEL

There is not set default for this setting. It allows users to specify their own
notification language.

Example model in a `languages` app::

```python
from django.conf import settings

class Language(models.Model):

    user = models.ForeignKey(User)
    language = models.CharField(max_length=10, choices=settings.LANGUAGES)
```

Setting this value in `settings.py`::

```python
PINAX_NOTIFICATIONS_LANGUAGE_MODEL = "languages.Language"
```

Formerly named `NOTIFICATION_LANGUAGE_MODULE`.

#### DEFAULT_FROM_EMAIL

Defaults to `webmaster@localhost` and is a [standard Django setting](https://docs.djangoproject.com/en/1.7/ref/settings/#default-from-email).

Default e-mail address to use for various automated correspondence from
`pinax.notifications.backends.email`.

#### LANGUAGES

Defaults to a tuple of all available languages and is a
[standard Django setting](https://docs.djangoproject.com/en/1.7/ref/settings/#languages).

The default for this is specifically used for things like the Django admin.
However, if you need to specify a subset of languages for your site's front end
you can use this setting to override the default. In which case this is the
definated pattern of usage::

```python
gettext = lambda s: s

LANGUAGES = (
    ("en", gettext("English")),
    ("fr", gettext("French")),
)
```

#### PINAX_NOTIFICATIONS_QUEUE_ALL

It defaults to `False`.

By default, calling `notification.send` will send the notification immediately,
however, if you set this setting to True, then the default behavior of the
`send` method will be to queue messages in the database for sending via the
`emit_notices` command.

Formerly named `NOTIFICATION_QUEUE_ALL`.

#### PINAX_NOTIFICATIONS_LOCK_WAIT_TIMEOUT

It defaults to `-1`.

It defines how long to wait for the lock to become available. Default of -1
means to never wait for the lock to become available. This only applies when
using crontab setup to execute the `emit_notices` management command to send
queued messages rather than sending immediately.

Formerly named `NOTIFICATION_LOCK_WAIT_TIMEOUT`.

### Scoping Notifications

Sometimes you have a site that has groups or teams. Perhaps you are using
[pinax-teams](https://github.com/pinax/pinax-teams/). If this is the case you
likely want users who might be members of multiple teams to be able to set
their notification preferences on a per team or group basis.

You will need to to simply override `NoticeSettingsView` to provide your own
scoping object.

#### Override NoticeSettingsView

I think it's best if we just demonstrate via code:

```python
# views.py

from pinax.notifications.views import NoticeSettingsView


class TeamNoticeSettingsView(NoticeSettingsView):
    
    @property
    def scoping(self):
        return self.request.team
```

Then override the url:

```python
# urls.py

from django.conf.urls import url

from .views import TeamNoticeSettingsView


urlpatterns = [
    # other urls
    url(r"^notifications/settings/$", TeamNoticeSettingsView.as_view(), name="notification_notice_settings"),
]
```

## Change Log

### 6.0.0

* Drop Django 1.11, 2.0, and 2.1, and Python 2,7, 3.4, and 3.5 support
* Add Django 2.2 and 3.0, and Python 3.6, 3.7, and 3.8 support
* Update packaging configs
* Direct users to community resources

### 5.0.2

* Remove unneeded compatibility

### 5.0.1

* Fix bytestring decoding bug
* Update django>=1.11 in requirements
* Update CI config
* Add sorting guidance for 3rd-party app imports
* Improve documentation and markup

### 5.0.0

* Standardize documentation layout
* Drop Django v1.8, v1.10 support

### 4.1.2

* Fix another silly documentation error

### 4.1.1

* Fix installation documentation

### 4.1.0

* Add Django 2.0 compatibility testing
* Drop Django 1.9 and Python 3.3 support
* Move documentation into README
* Convert CI and coverage to CircleCi and CodeCov
* Add PyPi-compatible long description

### 4.0
* _*BI*_: To support changes to `render_to_string` in Django 1.10 and above,
your notice `full.txt` and `short.txt` plain text templates must now be autoescaped explicitly using the
`{% autoescape %}` tag.
([#68](https://github.com/pinax/pinax-notifications/issues/68#issuecomment-258383323)) 

### 3.0.1
* initial support for Django 1.10

### 3.0
* fix compatability with Django migrations

### 2.1.0
* add Django migrations

### 2.0

* renamed app as pinax-notifications
* added the ability to override NoticeSetting model
* added documentation on scoping notifications

### 1.1.1

* fixed a deprecation warning

### 1.1

* added Russian locale
* added travis integration for tests/lints
* added created_notice_type wrapper
* cleaned up some small bugs identified by pylint

### 1.0

* removed unused `message.py` module
* removed `captureas` templatetag
* added `notice_settings.html` template
* other minor fixes and tweaks, mostly to code style

### 0.3

* pluggable backends

### 0.2.0

* _*BI*_: renamed Notice.user to Notice.recipient
* _*BI*_: renamed {{ user }} context variable in notification templates to
  {{ recipient }}
* _*BI*_: added nullable Notice.sender and modified send_now and queue to take
  an optional sender
* added received and sent methods taking a User instance to Notice.objects
* New default behavior: single notice view now marks unseen notices as seen
* no longer optionally depend on mailer; use django.core.mail.send_mail and
  we now encourge use of Django 1.2+ for mailer support
* notifications are not sent to inactive users
* users which do not exist when sending notification are now ignored
* _*BI*_: split settings part of notices view to its own view notice_settings

### 0.1.5

* added support for DEFAULT_HTTP_PROTOCOL allowing https absolute URLs

_*BI*_ = backward incompatible change


## History

This app was originally named `django-notification` but was renamed to
bring a common package name like `notification` under the `pinax` namespace
to avoid conflicts with other like named packages.

In addition, we wanted to take the opportunity to rename it to the plural
form, `notifications` to be in line with the convention we've adopted
across the ecosystem.


## Contribute

[Contributing](https://github.com/pinax/.github/blob/master/CONTRIBUTING.md) information can be found in the [Pinax community health file repo](https://github.com/pinax/.github).


## Code of Conduct

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a [Code of Conduct](https://github.com/pinax/.github/blob/master/CODE_OF_CONDUCT.md). We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.


## Connect with Pinax

For updates and news regarding the Pinax Project, please follow us on Twitter [@pinaxproject](https://twitter.com/pinaxproject) and check out our [Pinax Project blog](http://blog.pinaxproject.com).


## License

Copyright (c) 2012-present James Tauber and contributors under the [MIT license](https://opensource.org/licenses/MIT).
