from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import feed

from notification.models import *
from notification.decorators import basic_auth_required, simple_basic_auth_callback
from notification.feeds import NoticeUserFeed


@basic_auth_required(realm="Notices Feed", callback_func=simple_basic_auth_callback)
def feed_for_user(request):
    """
    An atom feed for all unarchived :model:`notification.Notice`s for a user.
    """
    url = "feed/%s" % request.user.username
    return feed(request, url, {
        "feed": NoticeUserFeed,
    })


@login_required
def notices(request, template_name="notification/notices.html"):
    """
    The main notices index view.
    
    Template: :template:`notification/notices.html`
    
    Context:
    
        notices
            A list of :model:`notification.Notice` objects that are not archived
            and to be displayed on the site.
    """
    notices = Notice.objects.notices_for(request.user, on_site=True)
    
    return render_to_response(template_name, {
        "notices": notices,
    }, context_instance=RequestContext(request))


@login_required
def notice_settings(request, template_name="notification/notice_settings.html"):
    """
    The notice settings view.
    
    Template: :template:`notification/notice_settings.html`
    
    Context:
        
        notice_types
            A list of all :model:`notification.NoticeType` objects.
        
        notice_settings
            A dictionary containing ``column_headers`` for each ``NOTICE_MEDIA``
            and ``rows`` containing a list of dictionaries: ``notice_type``, a
            :model:`notification.NoticeType` object and ``cells``, a list of
            tuples whose first value is suitable for use in forms and the second
            value is ``True`` or ``False`` depending on a ``request.POST``
            variable called ``form_label``, whose valid value is ``on``.
    """
    notice_types = NoticeType.objects.all()
    settings_table = []
    for notice_type in notice_types:
        settings_row = []
        for medium_id, medium_display in NOTICE_MEDIA:
            form_label = "%s_%s" % (notice_type.label, medium_id)
            setting = get_notification_setting(request.user, notice_type, medium_id)
            if request.method == "POST":
                if request.POST.get(form_label) == "on":
                    if not setting.send:
                        setting.send = True
                        setting.save()
                else:
                    if setting.send:
                        setting.send = False
                        setting.save()
            settings_row.append((form_label, setting.send))
        settings_table.append({"notice_type": notice_type, "cells": settings_row})
    
    if request.method == "POST":
        next_page = request.POST.get("next_page", ".")
        return HttpResponseRedirect(next_page)
    
    notice_settings = {
        "column_headers": [medium_display for medium_id, medium_display in NOTICE_MEDIA],
        "rows": settings_table,
    }
    
    return render_to_response(template_name, {
        "notice_types": notice_types,
        "notice_settings": notice_settings,
    }, context_instance=RequestContext(request))


@login_required
def single(request, id, mark_seen=True, template_name="notification/single.html"):
    """
    Detail view for a single :model:`notification.Notice`.
    
    Template: :template:`notification/single.html`
    
    Context:
    
        notice
            The :model:`notification.Notice` being viewed
    
    Optional arguments:
    
        mark_seen
            If ``True``, mark the notice as seen if it isn't
            already.  Do nothing if ``False``.  Default: ``True``.
    """
    notice = get_object_or_404(Notice, id=id)
    if request.user == notice.recipient:
        if mark_seen and notice.unseen:
            notice.unseen = False
            notice.save()
        return render_to_response(template_name, {
            "notice": notice,
        }, context_instance=RequestContext(request))
    raise Http404


@login_required
def archive(request, noticeid=None, next_page=None):
    """
    Archive a :model:`notices.Notice` if the requesting user is the
    recipient or if the user is a superuser.  Returns a
    ``HttpResponseRedirect`` when complete.
    
    Optional arguments:
    
        noticeid
            The ID of the :model:`notices.Notice` to be archived.
        
        next_page
            The page to redirect to when done.
    """
    if noticeid:
        try:
            notice = Notice.objects.get(id=noticeid)
            if request.user == notice.recipient or request.user.is_superuser:
                notice.archive()
            else:   # you can archive other users' notices
                    # only if you are superuser.
                return HttpResponseRedirect(next_page)
        except Notice.DoesNotExist:
            return HttpResponseRedirect(next_page)
    return HttpResponseRedirect(next_page)


@login_required
def delete(request, noticeid=None, next_page=None):
    """
    Delete a :model:`notices.Notice` if the requesting user is the recipient
    or if the user is a superuser.  Returns a ``HttpResponseRedirect`` when
    complete.
    
    Optional arguments:
    
        noticeid
            The ID of the :model:`notices.Notice` to be archived.
        
        next_page
            The page to redirect to when done.
    """
    if noticeid:
        try:
            notice = Notice.objects.get(id=noticeid)
            if request.user == notice.recipient or request.user.is_superuser:
                notice.delete()
            else:   # you can delete other users' notices
                    # only if you are superuser.
                return HttpResponseRedirect(next_page)
        except Notice.DoesNotExist:
            return HttpResponseRedirect(next_page)
    return HttpResponseRedirect(next_page)


@login_required
def mark_all_seen(request):
    """
    Mark all unseen notices for the requesting user as seen.  Returns a
    ``HttpResponseRedirect`` when complete. 
    """
    
    for notice in Notice.objects.notices_for(request.user, unseen=True):
        notice.unseen = False
        notice.save()
    return HttpResponseRedirect(reverse("notification_notices"))
