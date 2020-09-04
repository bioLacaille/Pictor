from django.core.mail import EmailMessage
from email.header import make_header
import os
from django.template import loader
from django.core.mail.backends.smtp import EmailBackend
from pictor.models import NotificationRule


class SendHtmlEmail(object):
    """send html email"""
    def __init__(self, subject, html_content, to_list, fail_silently=False, attachment=None,
                 cc_recipient=None, backend=None):
        self.subject = subject  # 主题
        self.html_content = html_content
        self.to_list = to_list
        self.attachment = attachment
        self.fail_silently = fail_silently  # 默认发送异常不报错
        self.cc_recipient = cc_recipient
        self.backend = backend

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, to=self.to_list, cc=self.cc_recipient,
                           connection=self.backend)
        msg.content_subtype = "html"  # Main content is now text/html
        if self.attachment:
            # 解决附件名称乱码: https://www.bbsmax.com/A/gVdnEoZ75W/
            for attachment in self.attachment:
                file_name = os.path.basename(attachment)
                msg.attach(make_header([(file_name, 'utf-8')]).encode('utf-8'), open(attachment, 'rb').read())
        msg.send(self.fail_silently)


def send_email(title, content, notify_level, to_list, fail_silently=False, attachment=None,
               cc_recipient=None, template='email_template.html'):
    notification_rule = NotificationRule.objects.get_active_notification_rule()
    if notification_rule:
        backend = EmailBackend(host=notification_rule.email_host, port=notification_rule.email_port,
                               username=notification_rule.email_host_user,
                               password=notification_rule.email_host_password, use_tls=notification_rule.email_user_ssl,
                               fail_silently=fail_silently)
        if template:
            html_content = loader.render_to_string(template, content)
        else:
            html_content = content
        subject = f'({notify_level}) {title}'
        send_html_email = SendHtmlEmail(subject, html_content, to_list, fail_silently, attachment, cc_recipient, backend)
        send_html_email.run()
        return True
    else:
        return False
