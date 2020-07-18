from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from datetime import datetime




class CustomUserManager(UserManager):
    """ユーザーマネージャー"""
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル
    usernameを使わず、emailアドレスをユーザー名として使うようにしています。
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def username(self):
        return self.email

class Shops(models.Model):
    SHOP_CHOICES = (
    ('1', '八潮'),
    ('2', '東川口'),
    ('3', '三郷'),
    ('4', '竹ノ塚'),
    ('5', '山室'),
    ('6', '奥田'),
    )


    shop = models.CharField("店舗", max_length=3,choices=SHOP_CHOICES, blank=True,default=1)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    
    def __int__(self):
        return self.get_shop_display()

class UserData(models.Model):
    Position_CHOICES = (
    ('3', 'デリ'),
    ('6', 'メイク'),
    ('2', 'デリ/メイク'),
    ('1', '代行'),
    ('4', '自転車'),
    ('5', '車'),
    )
    position =models.CharField('ポジション',max_length=5,choices=Position_CHOICES, blank=True)
    date_of_birth = models.DateField("生年月日",blank=True,default=datetime(1999, 1, 1))
    start_day = models.DateField("入店日",blank=True,default=datetime(2010, 1, 1))
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    no = models.CharField(max_length=3,blank=True)
    @property
    def age(self):
        if self.date_of_birth is None:
            return None
            today = date.today()
            age = today.year - self.date_of_birth.year
        if today < self.__yearbirthday(self.date_of_birth, today.year):
            age -= 1
            return age

        def __yearbirthday(self, date_of_birth, year):
            try:
                return date_of_birth.replace(year=year)
            except ValueError:
                date_of_birth += timedelta(days=1)
                return date_of_birth.replace(year=year)
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
