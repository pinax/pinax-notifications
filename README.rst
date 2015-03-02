pinax-notifications
===================

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/pinax/pinax-notifications
   :target: https://gitter.im/pinax/pinax-notifications?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

This app was originally named `django-notification` but was renamed to
bring a common package name like `notification` under the `pinax` namespace
to avoid conflicts with other like named packages.

In addition, we wanted to take the opportunity to rename it to the plural
form, `notifications` to be in line with the convention we've adopted
across the ecosystem.

This app was developed as part of the Pinax ecosystem but is just a Django app
and can be used independently of other Pinax apps.

To learn more about Pinax, see <http://pinaxproject.com/>


.. image:: https://badges.gitter.im/Join%20Chat.svg
    :target: https://gitter.im/pinax/django-notification

.. image:: https://img.shields.io/travis/pinax/pinax-notifications.svg
    :target: https://travis-ci.org/pinax/pinax-notifications

.. image:: https://img.shields.io/coveralls/pinax/pinax-notifications.svg
    :target: https://coveralls.io/r/pinax/pinax-notifications

.. image:: https://img.shields.io/pypi/dm/pinax-notifications.svg
    :target:  https://pypi.python.org/pypi/pinax-notifications/

.. image:: https://img.shields.io/pypi/v/pinax-notifications.svg
    :target:  https://pypi.python.org/pypi/pinax-notifications/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/pinax-notifications/


Many sites need to notify users when certain events have occurred and to allow
configurable options as to how those notifications are to be received.

The project aims to provide a Django app for this sort of functionality. This
includes:

* Submission of notification messages by other apps
* Notification messages on signing in
* Notification messages via email (configurable by user)
* Ability to supply your own backends notification channels


Running the Tests
------------------------------------

::

    $ pip install detox
    $ detox
