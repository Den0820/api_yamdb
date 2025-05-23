from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import PROJECT_MAIL
from users.models import CustomUser


def verification(cur_user, cur_email):
    user = get_object_or_404(CustomUser, username=cur_user)

    if user.email != cur_email:
        raise ValidationError(
            'Данный email соотвествует другому пользователю!')

    verification_code = CustomUser.objects.make_random_password()
    user.confirmation_code = verification_code
    user.save()

    send_mail(
        subject='Верификация',
        message=verification_code,
        from_email=PROJECT_MAIL,
        recipient_list=[user.email, ],
        fail_silently=True,
    )
