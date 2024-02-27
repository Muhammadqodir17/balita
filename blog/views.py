from django.shortcuts import render, redirect
from blog.models import Contact, Post, Comment, Category
from django.core.paginator import Paginator
from django.db.models import Q


def home_view(request):
    pp = Post.objects.filter(is_published=True).order_by("-created_at")
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

    data = Post.objects.filter(is_published=True)
    page = Paginator(data, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    base = Post.objects.filter(is_published=True).order_by("-created_at")

    # data = request.GET
    # cat = data.get('cat')
    # page = data.get('page', 1)
    # search_post = request.GET.get('search')
    # if search_post:
    #     post = Post.objects.filter(Q(title__icontains=search_post) & Q(content__icontains=search_post))
    # else:
    #     post = Post.objects.all().order_by('-created_at')

    d = {
        'page': page,
        'pp': pp,
        'posts': posts,
        'base': base,
        'home': 'active',
        'categories': categories
    }
    return render(request, 'index.html', context=d)


def category_view(request):
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

    data = request.GET
    cat = data.get('category')
    if cat:
        category = Category.objects.get(name=cat)
        data = Post.objects.filter(is_published=True, category=category)
        page = Paginator(data, 2)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
    else:
        category = Category.objects.get(name=cat)
        data = Post.objects.filter(is_published=True)
        page = Paginator(data, 2)
        page_list = request.GET.get('page')
        page = page.get_page(page_list)
    d = {
        'posts': posts,
        'base': base,
        'page': page,
        'category': category,
        'categories': categories,
        'categoriess': 'activate'
    }
    return render(request, 'category.html', context=d)


def blog_single_detail_view(request, pk):
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(post_id=pk, name=data['name'], email=data['email'],message=data['message'])
        obj.save()
        return redirect(f'/blog/{pk}')
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk)
    return render(request, 'blog-single.html', context={'posts': posts, 'base': base, 'post': post, 'comments': comments, 'categories': categories})


def about_view(request):
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    data = Post.objects.filter(is_published=True).order_by('-created_at')
    page = Paginator(data, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    data = request.GET
    category = data.get("cat")
    if category:
        post = Post.objects.filter(is_published=True, category_id=category)
    else:
        post = Post.objects.filter(is_published=True)
    categories = Category.objects.all()
    d = {
        'page': page,
        'base': base,
        'post': post,
        'about': 'active',
        'categories': categories,
    }
    return render(request, 'about.html', context=d)


def contact_view(request):
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    d = {
        'posts': posts,
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
