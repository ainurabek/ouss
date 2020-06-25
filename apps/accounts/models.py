from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save

GENDER_CHOICES = (
        ('M', 'Муж'),
        ('F', 'Жен'),
    )
class Role(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'пользовательские роли'

    def __str__(self):
        return self.name

class DepartmentKT(models.Model):
    name = models.CharField('Отдел', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name

class SubdepartmentKT(models.Model):
    department = models.ForeignKey(DepartmentKT, verbose_name='Подотдел',
                                  null=True, blank=True, related_name='supdepartment',
                                  on_delete=models.CASCADE)
    name = models.CharField('Подотдел', max_length=30, blank=True)

    class Meta:
        verbose_name = 'Подотдел'
        verbose_name_plural = 'Подотделы'

    def __str__(self):
        return self.name

class UserManager(BaseUserManager):
    def create_user(self, username, role=None, department=None, subdepartment=None, password=None, is_staff=False, is_active=True, is_admin=False):
        if not username:
            raise ValueError('users must have a username')
        if not password:
            raise ValueError('user must have a password')



        user_obj = self.model(
            username=username,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.role = role
        user_obj.department = department
        user_obj.subdepartment = subdepartment
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,

        )
        return user

    def create_superuser(self, username, password=None, is_admin=True, is_staff=True, is_active=True, role=None):
        user = self.create_user(
            username,
            password=password,
            is_staff=True,
            is_admin=True,
            is_active=True,
        )
        user.set_password(password)

        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active

        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username=models.CharField(unique=True, max_length=30)
    active = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, verbose_name='Роль пользователя',
                                  null=True, blank=True, related_name='users_role',
                                  on_delete=models.CASCADE)
    department = models.ForeignKey(DepartmentKT, verbose_name='Отдел пользователя',
                                  null=True, blank=True, related_name='users_department',
                                  on_delete=models.CASCADE)
    subdepartment = models.ForeignKey(SubdepartmentKT, verbose_name='Подотдел пользователя',
                                  null=True, blank=True, related_name='users_subdepartment',
                                  on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        return super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField('Должность', max_length=30, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=30, blank=True, null=True)
    last_name = models.CharField('Фамилия', max_length=30, blank=True, null=True)
    middle_name = models.CharField('Отчество', max_length=30, null=True, blank=True)
    online = models.BooleanField('В сети', default=False)
    gender = models.CharField('Пол', max_length=10, blank=True, null=True,
                              choices=GENDER_CHOICES)
    phone_number = models.CharField('Рабочий номер телефона', max_length=50, null=True, blank=True)


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Log(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name="log_profile")
    start_at = models.DateTimeField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журнал'

    def __str__(self):
        return f"{self.user.first_name}"


def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.created(user=kwargs['instance'])

    post_save.connect(createProfile, sender=User)
