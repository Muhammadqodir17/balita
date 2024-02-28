from django.contrib import admin
from blog.models import Category, Post, Comment, Contact, Tag

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Tag)
