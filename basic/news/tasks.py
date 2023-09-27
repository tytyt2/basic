from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from django.core.mail import EmailMultiAlternatives
from .models import Post, User, Category
from django.conf import settings


@shared_task
def new_post(post_pk):

    post = Post.objects.get(pk=post_pk)

    preview=Post.text
    title=Post.title

    user_emails= User.objects.values_list('email', flat=True)

    if user_emails:

        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': preview,
                'link': f'{settings.SITE_URL}/{post.pk}'
            }
        )
        msg = EmailMultiAlternatives(
            subject = title,
            body ='',
            from_email= settings.DEFAULT_FROM_EMAIL,
            to = user_emails
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()


@shared_task
def weekly_news():
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        last_posts = Post.objects.filter(postCategory=category).order_by('-dateCreation')[:5]

        html_content = render_to_string(
            'post_created_email.html',
            {
                'last_posts': last_posts,
                'Категория': f'{category.name}'
            }
        )

        for subscriber in subscribers:
            msg = EmailMultiAlternatives(
                subject=f"Еженедельная рассылка новостей ({category.name})",
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email]
            )
            msg.attach_alternative(html_content, 'text/html')
            msg.send()








