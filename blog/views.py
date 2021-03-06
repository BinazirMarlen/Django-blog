
from django.shortcuts import render, redirect

from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .form import UserRegister, UserLoginform
from django.contrib.auth import login, logout
from django.views.generic import ListView

def post_list(request):
    posts = Post.objects.order_by('-published_date')
    return render(request, 'blog/list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def register(request):
    if request.method=='POST':
        form=UserRegister(request.Post)
        if form.is_valid():
            messages.success(request, 'Registered')
            return redirect('list')
        else:
            messages.error(request,'error')
    else:
        form=UserRegister()
    return render(request, 'blog/register.html',{'form':form})


def user_login(request):
    if request.method=='POST':
        form=UserLoginform(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)

            return redirect('list')
        else:
            messages.error(request,'error')
            form=UserLoginform()
    else:
        form=UserLoginform()
    return render(request, 'blog/login.html',{'form':form})
        

def user_logout(request):
    logout(request)
    return redirect('login')

class Search(ListView):
    template_name='blog/search.html'
    context_object_name='posts'

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('search'))
    def get_context_data(self, *, object_list=None, **kwargs):
        context= super().get_context_data(**kwargs)
        return context

class Sort(ListView):
    template_name='blog/sort.html'
    context_object_name='posts'

    def get_queryset(self):
        if self.request.GET.get('Sort by published date')=='date':
            return Post.objects.order_by('-published_date')
        else:
            return Post.objects.order_by('title')
           
    def get_context_data(self, *, object_list=None, **kwargs):
        context= super().get_context_data(**kwargs)
        return context