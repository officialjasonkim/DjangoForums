from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post, Reply
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, TemplateView
from django.urls import reverse
import math

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'forum/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'forum/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "forum/user.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = User.objects.get(username=self.kwargs['username'])
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Reply
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = Post.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        return context

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Reply
    fields = ['content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Reply.objects.get(pk=self.kwargs['pk']).post
        return context

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Reply
    success_url = ''

    # def __init__(self, *args, **kwargs):
    #     id = Reply.objects.get(pk=self.kwargs['pk']).post,id
    #     success_url = '/post/' + id + '/'

    def test_func(self):
        id = Reply.objects.get(pk=self.kwargs['pk']).post.id
        self.success_url = '/post/' + str(id) + '/'
        reply = self.get_object()
        if self.request.user == reply.author:
            return True
        return False

def devlog(request):
    context = {
        'title': "Devlog"
    }
    return render(request, 'forum/devlog.html', context)

def about(request):
    context = {
        'title': "About"
    }
    return render(request, 'forum/about.html', context)

def back(request, post_pk):
    page = 1
    counter = -1
    posts = reversed(Post.objects.all())
    for post in posts:
        counter += 1
        if post.pk == post_pk:
            break
    page += int(math.floor(counter/5))
    return HttpResponseRedirect('/?page='+str(page))