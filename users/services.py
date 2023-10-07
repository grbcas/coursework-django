from django.core.mail import send_mail


def send_new_password(*args):
    send_mail(
        subject='Верификация почты',
        message=f'перейдите по ссылке: '
                f'http://{current_site}/users/verification?verification_key={verification_key}\n ',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[new_user.email]
    )