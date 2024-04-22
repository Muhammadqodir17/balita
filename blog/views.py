from django.shortcuts import render, redirect
from blog.models import Contact, Post, Comment, Category, Tag
from django.core.paginator import Paginator


def home_view(request):
    data = Post.objects.filter(is_published=True)
    page = Paginator(data, 6)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    tags = Tag.objects.all()
    pp = Post.objects.filter(is_published=True).order_by("-created_at")
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

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
        'tags': tags,
        'pp': pp,
        'posts': posts,
        'base': base,
        'home': 'active',
        'categories': categories
    }
    return render(request, 'index.html', context=d)


def category_view(request):
    tags = Tag.objects.all()
    base = Post.objects.filter(is_published=True).order_by("-created_at")
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

    data = request.GET
    tag = data.get('tags')
    name = data.get('category')

    if tag:
        post = Post.objects.filter(is_published=True, tag=tag)
    else:
        post = Post.objects.filter(is_published=True)

    if name:
        category = Category.objects.filter(name=name).first()
    else:
        category = Category.objects.filter()

    posts_cat = Post.objects.filter(is_published=True, category=category)

    # category = Category.objects.get(name=name)
    page = data.get('page', 1)
    page_obj = Paginator(posts_cat, 2)

    # else:
    #     post = Post.objects.filter(is_published=True)
    # page = Paginator(post, 2)
    # page_list = request.GET.get('page')
    # pah = page.get_page(page_list)
    # pah = page.get_page(page)

    d = {
        'posts': posts,
        'post': post,
        'category': category,
        'tags': tags,
        'base': base,
        'page': page_obj.page(page),
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
        return redirect(f'/blog/{pk}')
    post = Post.objects.get(id=pk)
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
    data = request.GET
    category = data.get("cat")
    if category:
        post = Post.objects.filter(is_published=True, category_id=category)
    else:
        post = Post.objects.filter(is_published=True)
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
    posts = Post.objects.filter(is_published=True)
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

#
# def tags_view(request, pk):
#     tags = Tag.objects.get(id=pk)
#     posts = Post.objects.filter(is_published=True, tag=tags)
#     d = {
#         'posts': posts,
#         'tags_name': tags.name
#     }
#     return render(request, "category.html", context=d)


def search_view(request):
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        posts = Post.objects.filter(is_published=True, title__icontains=query)
    else:
        posts = Post.objects.filter(is_published=True)
    context = {
        'posts': posts,
        'categories': Category.objects.all()
    }

    return render(request, 'category.html', context=context)
