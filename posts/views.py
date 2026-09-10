
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator

from posts.forms import PostCreateForm
from posts.models import Post

# Create your views here.

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:post-detail', pk=post.id)
    else:
        form = PostCreateForm()
    return render(request, 'posts/post_creation.html', {'form':form})



@login_required
def get_all_user_posts(request):
    post_list = Post.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/post_list.html', {'page_obj':page_obj})



def feed_posts(request):
    post_list = Post.objects.all().order_by('-created_at')
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/post_feed.html', {'page_obj':page_obj})
    


def detail_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post':post})



@login_required
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user.id != request.user.id:
        return HttpResponseForbidden("This is not your own post...")
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post-detail', pk=pk)
    else:
        form = PostCreateForm(instance=post)
    return render(request, 'posts/post_update.html', {'form':form,'post':post})


@login_required 
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.user != request.user:
        return HttpResponseForbidden("This is not your own post...")
    if request.method == 'POST':
        post.delete()
        return render(request, 'posts/post_delete_success.html')
    else:
        return render(request, 'posts/post_confirm_delete.html', {'post':post})
        






