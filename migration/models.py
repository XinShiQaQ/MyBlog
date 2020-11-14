from django.db import models
# Create your models here.


class User(models.Model):
    account = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    name = models.CharField(max_length=20, unique=True)


class Category(models.Model):
    """
    分类名
    """
    categoryName = models.CharField(max_length=20, unique=True)


class Tag(models.Model):
    """
    Tag名
    """
    tagName = models.CharField(max_length=20, unique=True)


class Post(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()

    createTime = models.DateTimeField()
    modifiedTime = models.DateTimeField()

    excerpt = models.CharField(max_length=100)  # 摘录

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class WebsiteSettings(models.Model):
    websiteName = models.CharField(max_length=20)
    websiteUser = models.ForeignKey(User, on_delete=models.CASCADE)
