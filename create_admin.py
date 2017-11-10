import django
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audiencias_publicas.settings")


def create_superuser():
    from django.contrib.auth import get_user_model
    User = get_user_model()

    admin_email = os.environ.get('ADMIN_EMAIL', None)
    admin_username = os.environ.get('ADMIN_USERNAME', None)
    admin_passwd = os.environ.get('ADMIN_PASSWORD', None)

    if None not in [admin_email, admin_passwd, admin_username]:
        print('Creating superuser...')
        user = User.objects.get_or_create(email=admin_email,
                                          username=admin_username)[0]
        user.set_password(admin_passwd)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print('Done!')
    else:
        print('Missing ADMIN_EMAIL, ADMIN_USERNAME or ADMIN_PASSWORD '
              'environment variable.')
        sys.exit(1)


if __name__ == '__main__':
    django.setup()
    create_superuser()
