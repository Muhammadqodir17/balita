from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import home_view, category_view, about_view, contact_view, blog_single_detail_view, search_view

urlpatterns = [
    path('', home_view, name='home'),
    path('category/', category_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('blog/<int:pk>/', blog_single_detail_view),
    path('search/', search_view),
    # path('tags/<int:pk>/', tags_view)
]
