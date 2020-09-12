from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            # email = 'admin@lottee.com'
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('locale', 'ru')
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('locale', 'en')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ User model """
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(verbose_name='name', max_length=255)
    image = models.ImageField(verbose_name='Аватар', upload_to='user/', blank=True, null=True)

    locale = models.CharField(verbose_name='Локация', max_length=16, default='ru')
    language = models.CharField(verbose_name='Язык системы', max_length=16, default='ru')
    energy = models.PositiveSmallIntegerField(verbose_name='Энергия', default=15)
    karma = models.SmallIntegerField(verbose_name='Карма пользователя', default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = UserManager()

    def __str__(self):
        return self.email


class Address(models.Model):
    """ User Address model """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    index = models.CharField(max_length=24, null=True)
    country = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)
    district = models.CharField(max_length=64, null=True)
    street = models.CharField(max_length=64, null=True)
    house = models.CharField(max_length=16, null=True)
    phone_number = models.CharField(max_length=32, null=True)

    def __str__(self):
        return 'country %s city %s' % (self.country, self.city)
