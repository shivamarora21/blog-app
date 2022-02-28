from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

# posts = [
#     {
#         'author': 'ShivamA',
#         'title': 'Blog Post',
#         'content': 'First post content',
#         'date_posted': 'Feburary 26, 2022'
#     },
#     {
#         'author': 'Shivam',
#         'title': 'Blog Post 2',
#         'content': 'First post content 2',
#         'date_posted': 'Feburary 28, 2022'
#     }
# ]

# function based views
def home(request):
    context = {
        'title': 'First One',
        # 'posts': posts
        'posts': Post.objects.all()

    }
    return render(request, 'blog/home.html', context)

# class based view
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #by default it looks for <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']  #['date_posted]
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  #by default it looks for <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})