from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from post.models import Post

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=MyUserManager.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, date_of_birth, password):
        u = self.create_user(username,
                        password=password,
                        date_of_birth=date_of_birth
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u


class MyUser(AbstractBaseUser):
    email = models.EmailField(
                        verbose_name='email address',
                        max_length=255,
                        unique=True,
                    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    @property
    def is_staff(self):
        return self.is_admin


class UserStorage(models.Model):
    user = models.ForeignKey(MyUser, related_name='user')
    posts = models.ManyToOneRel(Post, on_delete=models.CASCADE, related_name='posts')
