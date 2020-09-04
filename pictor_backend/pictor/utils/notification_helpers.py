from pictor.models import User
from pictor.configures import NOTIFY_INFO


def send_notify(title, content, content_object=None, recipient=None, level=NOTIFY_INFO, sender=None,
                remark=None, fail_silently=False, attachment=None, cc_recipient=None):
    if not recipient:
        recipient = []
    if not attachment:
        attachment = []
    if not cc_recipient:
        cc_recipient = []
    kw = {
        'title': title,
        'content': content,
        'level': level,
        'remark': remark,
        'fail_silently': fail_silently,
        'attachment': attachment,
        'cc_recipient': cc_recipient
    }

    if content_object:
        kw['object_type'] = content_object._meta.model_name
        kw['object_id'] = content_object.id

    if sender:
        kw['sender'] = sender.id if isinstance(sender, User) else sender

    if recipient and isinstance(recipient[0], User):
        kw['recipient'] = [rec.id for rec in recipient]
    else:
        kw['recipient'] = recipient
    from pictor.tasks import send_notify_task
    return send_notify_task.delay(**kw)
