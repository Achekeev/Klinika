from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None, staff=False, active=True, admin=False):
        if not phone:
            raise ValueError('users must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user_obj = self.model(
            phone=phone,
            name=name,
        )
        user_obj.set_password(password)
        user_obj.staff = staff
        user_obj.admin = admin
        user_obj.active = active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, name, password=None):
        user = self.create_user(
            phone,
            name,
            password=password,
            staff=True,
        )
        return user

    def create_superuser(self, phone, name, password=None):
        user = self.create_user(
            phone,
            name,
            password=password,
            staff=True,
            admin=True,
        )
        return user


CHOICES = [
    ('MD', 'Media'),
    ('SN', 'Social_Network'),
    ('RS', 'RELATIVES'),
    ('D', 'Doctor'),
    ('OP', 'Operated_Here'),
    ('E', 'Else')
]


class Client(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,20}$', message='+996111222333')
    phone = models.CharField(validators=[phone_regex], max_length=30, unique=True)
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    last_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True)
    birth_date = models.DateField(auto_now=False, null=True, blank=True)
    email = models.EmailField(null=True)
    age = models.CharField(max_length=3, null=True)
    clinic_find = models.CharField(max_length=255, verbose_name='Откуда узнали', choices=CHOICES)
    active = models.BooleanField(default=False, verbose_name='is active')
    staff = models.BooleanField(default=False, verbose_name='is staff')
    admin = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', ]

    objects = UserManager()

    def __str__(self):
        return f'{self.phone}-{self.name}'

    def get_name(self):
        return self.phone

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class PhoneOTP(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,20}$', message="Phone number must be entered in the format")
    phone = models.CharField(validators=[phone_regex], max_length=21, unique=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    count = models.IntegerField(default=0, help_text='Number of otp sent')
    logged = models.BooleanField(default=False, help_text='If otp verification got successful')
    forgot = models.BooleanField(default=False, help_text='only true for forgot password')
    forgot_logged = models.BooleanField(default=False, help_text='Only true if validate otp forgot get successful')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)

    class Meta:
        verbose_name = 'Активационный код'
        verbose_name_plural = 'Активационный код'

