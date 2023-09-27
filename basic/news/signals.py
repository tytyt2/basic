from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed, post_init
from django.dispatch import receiver
from django.template.loader import render_to_string

from .tasks import new_post

from .models import *
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject = title,
        body ='',
        from_email= settings.DEFAULT_FROM_EMAIL,
        to = subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs ):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


@receiver(post_save, sender=Post)
def test(sender, instance, created, **kwargs):
    if created:
        new_post.delay(instance.pk)






# @receiver(post_save, sender=Post)
# def product_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.postCategory
#     ).values_list('email', flat=True)
#
#     subject = f'Новая статья в категории {instance.postCategory}'
#
#     text_content = (
#         f'Статья: {instance.title}\n'
#         f'Рейтинг: {instance.rating}\n\n'
#         f'Ссылка на статью: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Товар: {instance.title}<br>'
#         f'Цена: {instance.rating}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на товар</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()