from handy_man.apps.user_profile.models import UserProfile
from django.contrib.auth.models import User
from handy_man.apps.user_profile.models import Profession


# Create users.
def create_users():
    from datetime import date
    n = 0
    profession = Profession.objects.create(qualified=True, profession_type='carpentry')
    while n < 40:
        if n < 20:
            account_type = 'artisan'
            profession=profession
        else:
            account_type = 'customer'
            profession = None
        user = User.objects.create(
            email='admin@gmail.com',
            first_name='user{0}'.format(n),
            last_name='user{0}'.format(n),
            username='user{0}'.format(n),
            password='usersusers{0}'.format(n),
            is_active=True,
            is_staff=True)
        print("password: ", 'usersusers{0}'.format(n))
        UserProfile.objects.create(
            user=user,
            mobile='7765769{0}'.format(n),
            email_validated=True,
            administrator_validated=True,
            gender='F',
            account_type=account_type,
            profession=profession,
            dob=date(1990, 12, 1),
        )
        n += 1
create_users()
