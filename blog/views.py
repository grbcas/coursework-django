from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog


# Create your views here.
class BlogCreateView(CreateView):

    model = Blog
    fields = ('title', 'body', 'image',)
    success_url = reverse_lazy('blog:list_blog')

    def form_valid(self, form):
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.slug = slugify(new_entry.title)
            new_entry.save()
            return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image')

    def form_valid(self, form):
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.slug = slugify(new_entry.title)
            new_entry.save()
            return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list_blog')

