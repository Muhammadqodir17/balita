from django.db import models
from config.base_models import BaseModel
from blog.validators import validate_uz_phone_number


class Tag(BaseModel):
    objects = None
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(BaseModel):

    objects = None
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Post(BaseModel):
    objects = None
    tag = models.ManyToManyField('Tag', blank=True, related_name='posts')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts/')
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name


class Contact(BaseModel):
    objects = None
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=13, validators=[validate_uz_phone_number], null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_solved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

