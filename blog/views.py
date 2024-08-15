import random

from django.db.models import Q
from django.shortcuts import render, redirect
from blog.models import Contact, Post, Comment, Category, Tag
from django.core.paginator import Paginator


def home_view(request):
    data = Post.objects.filter(is_published=True)
    page = Paginator(data, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    tags = Tag.objects.all()

    posts_for_second_one = Post.objects.filter(is_published=True).order_by("-created_at")
    posts_list_for_second_one = list(posts_for_second_one)
    random.shuffle(posts_list_for_second_one)

    posts = Post.objects.filter(is_published=True)
    posts_list = list(posts)
    random.shuffle(posts_list)

    categories = Category.objects.all()

    base = Post.objects.filter(is_published=True).order_by("-created_at")

    d = {
        'page': page,
        'tags': tags,
        'pp': posts_list_for_second_one[:3],
        'posts': posts_list[:3],
        'base': base,
        'home': 'active',
        'categories': categories
    }
    return render(request, 'index.html', context=d)


def category_view(request):
    tags = Tag.objects.all()
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    posts = Post.objects.filter(is_published=True).order_by('-view_count')[:3]
    categories = Category.objects.all()

    data = request.GET
    tag = data.get('tags')
    name = data.get('category')
    page_list = request.GET.get('page')
    cat_or_tag = 'Category'

    if tag:
        posts_cat = Post.objects.filter(tag__id=tag)
        cat_or_tag = 'Tags'
        category = None
    else:
        category = Category.objects.filter(id=name).first()
        posts_cat = Post.objects.filter(is_published=True, category=category)

    page = Paginator(posts_cat, 2)
    page = page.get_page(page_list)
    d = {
        'posts': posts,
        'category': category,
        'tags': tags,
        'base': base,
        'cat_or_tag': cat_or_tag,
        'page': page,
        'categories': categories,
    }
    return render(request, 'category.html', context=d)


def blog_single_detail_view(request, pk):
    tags = Tag.objects.all()
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data['name'], email=data['email'], message=data['message'])
        obj.save()
        plus_comment_to_post = Post.objects.filter(id=pk).first()
        plus_comment_to_post.comment_count += 1
        plus_comment_to_post.save(update_fields=['comment_count'])
        return redirect(f'/blog/{pk}')
    post = Post.objects.get(id=pk)
    post.view_count += 1
    post.save(update_fields=['view_count'])
    comments = Comment.objects.filter(post_id=pk)
    d = {
        'posts': posts,
        'tags': tags,
        'base': base,
        'post': post,
        'comments': comments,
        'categories': categories
    }
    return render(request, 'blog-single.html', context=d)


def about_view(request):
    tags = Tag.objects.all()
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    data = Post.objects.filter(is_published=True).order_by('-created_at')

    page = Paginator(data, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    post = Post.objects.filter(is_published=True).order_by('-view_count')[:3]
    categories = Category.objects.all()
    d = {
        'page': page,
        'tags': tags,
        'base': base,
        'post': post,
        'about': 'active',
        'categories': categories,
    }
    return render(request, 'about.html', context=d)


def contact_view(request):
    tags = Tag.objects.all()
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True).order_by('-view_count')[:3]
    d = {
        'posts': posts,
        'tags': tags,
        'base': base,
        'contact': 'active',
        'categories': categories
    }
    if request.method == 'POST':
        data = request.POST

        obj = Contact.objects.create(name=data.get('name'), email=data.get('email'), phone=data.get('phone'),
                                     message=data.get('message'))
        obj.save()
        return redirect('/contact')
    return render(request, 'contact.html', context=d)


def search_view(request):
    posts = Post.objects.all()
    post = Post.objects.filter(is_published=True).order_by('-view_count')
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        if Post.objects.filter(tag__name__icontains=query, is_published=True):
            posts = Post.objects.filter(tag__name__icontains=query, is_published=True)
        if Post.objects.filter(title__icontains=query, is_published=True):
            posts = Post.objects.filter(title__icontains=query, is_published=True)
        if Post.objects.filter(description__icontains=query, is_published=True):
            posts = Post.objects.filter(description__icontains=query, is_published=True)

    context = {
        'page': posts,
        'base': Post.objects.filter(is_published=True).order_by("-created_at"),
        'cat_or_tag': 'Posts',
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'posts': post[:3]
    }

    return render(request, 'category.html', context=context)
