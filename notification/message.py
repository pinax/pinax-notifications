from django.db.models import get_model
from django.utils.translation import ugettext

# a notice like "foo and bar are now friends" is stored in the database
# as "{auth.User.5} and {auth.User.7} are now friends".
#
# encode_object takes an object and turns it into "{app.Model.pk}" or
# "{app.Model.pk.msgid}" if named arguments are used in send()
# decode_object takes "{app.Model.pk}" and turns it into the object
#
# encode_message takes either ("%s and %s are now friends", [foo, bar]) or
# ("%(foo)s and %(bar)s are now friends", {'foo':foo, 'bar':bar}) and turns
# it into "{auth.User.5} and {auth.User.7} are now friends".
#
# decode_message takes "{auth.User.5} and {auth.User.7}" and converts it
# into a string using the given decode function to convert the object to
# string representation
#
# message_to_text and message_to_html use decode_message to produce a
# text and html version of the message respectively.

def encode_object(obj, name=None):
    encoded = "%s.%s.%s" % (obj._meta.app_label, obj._meta.object_name, obj.pk)
    if name:
        encoded = "%s.%s" % (encoded, name)
    return "{%s}" % encoded


def encode_message(message_template, objects):
    if objects is None:
        return message_template
    if isinstance(objects, list) or isinstance(objects, tuple):
        return message_template % tuple(encode_object(obj) for obj in objects)
    if type(objects) is dict:
        return message_template % dict((name, encode_object(obj, name)) for name, obj in objects.iteritems())
    return ""


def decode_object(ref):
    decoded = ref.split(".")
    if len(decoded) == 4:
        app, name, pk, msgid = decoded
        return get_model(app, name).objects.get(pk=pk), msgid
    app, name, pk = decoded
    return get_model(app, name).objects.get(pk=pk), None


class FormatException(Exception):
    pass


def decode_message(message, decoder):
    out = []
    objects = []
    mapping = {}
    in_field = False
    prev = 0
    for index, ch in enumerate(message):
        if not in_field:
            if ch == "{":
                in_field = True
                if prev != index:
                    out.append(message[prev:index])
                prev = index
            elif ch == "}":
                raise FormatException("unmatched }")
        elif in_field:
            if ch == "{":
                raise FormatException("{ inside {}")
            elif ch == "}":
                in_field = False
                obj, msgid = decoder(message[prev+1:index])
                if msgid is None:
                    objects.append(obj)
                    out.append("%s")
                else:
                    mapping[msgid] = obj
                    out.append("%("+msgid+")s")
                prev = index + 1
    if in_field:
        raise FormatException("unmatched {")
    if prev <= index:
        out.append(message[prev:index+1])
    result = "".join(out)
    if mapping:
        args = mapping
    else:
        args = tuple(objects)
    return ugettext(result) % args


def message_to_text(message):
    def decoder(ref):
        obj, msgid = decode_object(ref)
        return unicode(obj), msgid
    return decode_message(message, decoder)


def message_to_html(message):
    def decoder(ref):
        obj, msgid = decode_object(ref)
        if hasattr(obj, "get_absolute_url"): # don't fail silenty if get_absolute_url hasn't been defined
            return u"""<a href="%s">%s</a>""" % (obj.get_absolute_url(), unicode(obj)), msgid
        else:
            return unicode(obj), msgid
    return decode_message(message, decoder)
    