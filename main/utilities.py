from django.template.loader import render_to_string
from django.core.signing import Signer
from datetime import datetime
from os.path import splitext

from bboard.settings import ALLOWED_HOSTS

# ----------------------------------------------АВТОРИЗАЦИЯ-------------------------------------------------------#
signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    context = {
        'user': user,
        'host': host,
        'sign': signer.sign(user.username)  # Создание цифровой подписи
    }
    subject = render_to_string('email/activation_letter_subject.txt', context)
    body_text = render_to_string('email/activation_letter_body.txt', context)
    user.email_user(subject, body_text)
# ----------------------------------------------АВТОРИЗАЦИЯ-------------------------------------------------------#


# ----------------------------------------------ОБЪЯВЛЕНИЯ--------------------------------------------------------#
def get_timestamp_path(instance, filename):
    """Генерация имен сохраняемых в модели выгруженных файлов"""
    return f'{datetime.now().timestamp()}{splitext(filename)[1]}'
# ----------------------------------------------ОБЪЯВЛЕНИЯ--------------------------------------------------------#


# ----------------------------------------------КОММЕНТАРИИ-------------------------------------------------------#
def send_new_comment_notification(comment):
    if ALLOWED_HOSTS:
        host = 'https://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://localhost:8000'
    author = comment.bb.author
    bb_title = comment.bb.title
    context = {
        'author': author,
        'host': host,
        'comment': comment,
        'bb_title': bb_title,
    }
    subject = render_to_string('email/new_comment_letter_subject.txt', context)
    body_text = render_to_string('email/new_comment_letter_body.txt', context)
    author.email_user(subject, body_text)
# ----------------------------------------------КОММЕНТАРИИ-------------------------------------------------------#
