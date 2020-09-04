from pictor.models import Notification
from django.contrib.contenttypes.models import ContentType
from celery import shared_task
from pictor.configures import NOTIFY_INFO
from pictor.models import User, NotificationRule
from pictor.utils.applog_helpers import task_logger
from pictor.utils.email_helpers import send_email


@shared_task(name="send_notify_task")
def send_notify_task(title, content, object_type=None, object_id=None, sender=None, recipient=None, level=NOTIFY_INFO,
                     remark=None, fail_silently=False, attachment=None, cc_recipient=None):
    # 发送通知，同时发送消息通知跟邮件通知
    try:
        kwargs = {
            'title': title,
            'content': content,
            'remark': remark,
            'level': level,
        }
        models = ContentType.objects.filter(model=object_type).first()
        if models:
            content_object = models.get_object_for_this_type(id=object_id)
            kwargs['content_object'] = content_object
        if sender:
            sender = User.objects.get(pk=sender)
            kwargs['sender'] = sender
        notify_setting = NotificationRule.objects.get_active_notification_rule()
        recipient_list = User.objects.filter(id__in=recipient)
        task_logger.info(f'待发送消息数据包为{kwargs}')
        if notify_setting and notify_setting.is_notify:
            notify_list = []
            for recipient in recipient_list:
                kwargs['recipient'] = recipient
                Notification(**kwargs)
                notify_list.append(Notification(**kwargs))
            Notification.objects.bulk_create(notify_list)
            task_logger.info(f'成功发送站内消息')
        if notify_setting and notify_setting.is_email:
            to_list = [recipient.email for recipient in recipient_list if recipient.email]
            send_email(title=title, content=kwargs, notify_level=NotificationRule.objects.get_level_desc(level),
                       to_list=to_list, fail_silently=fail_silently, attachment=attachment, cc_recipient=cc_recipient)
            task_logger.info(f'成功发送邮件')
    except Exception as error:
        task_logger.error(f'发送消息通知发生错误:{error}')
