from django.db import models
from helpers.models import BaseModel
from accounts.models import MyUser

# Create your models here.


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def last(self):
        return self.get_queryset().last()


class PostQuerySet(models.QuerySet):
    def last(self):
        return self.filter(created_at__gte=datetime.date.today())


class Category(BaseModel):
    title = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, unique=True)
    icon = models.FileField(upload_to="category/")
    post_count = models.IntegerField(default=0)


class Post(BaseModel):
    title = models.CharField(max_length=128, verbose_name='Nomi')
    slug = models.SlugField(max_length=250, null=False, blank=False)
    content = models.TextField()
    image = models.ImageField(upload_to="post/", null=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    published_date = models.DateField(null=True)
    read_min = models.IntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    is_popular = models.BooleanField(default=False)
    object = PostManager()


