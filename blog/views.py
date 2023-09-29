from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Blog


class BlogListView(ListView):
    model = Blog


class BlogCreateView(CreateView):
    model = Blog


class BlogDetailView(DetailView):
    model = Blog


class BlogUpdateView(UpdateView):
    model = Blog


class BlogDeleteView(DetailView):
    model = Blog
