from django.urls import path
from django.views.decorators.cache import cache_page

from blog.apps import BlogConfig
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogDeleteView, BlogUpdateView

app_name = BlogConfig.name

urlpatterns = [
    path('blog', BlogListView.as_view, name='blog'),
    path('create_entry/', BlogCreateView.as_view(), name='create_entry'),
    path('delete_entry/<int:pk>/', BlogDeleteView.as_view(), name='delete_entry'),
    path('update_entry/<int:pk>/', BlogUpdateView.as_view(), name='update_entry'),
    path('entry_detail/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='entry_detail'),
]
