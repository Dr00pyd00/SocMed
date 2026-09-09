
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from posts.forms import PostCreateForm
from posts.models import Post

# Create your views here.


def test_view(request):
    return render(
            request,
            'posts/test.html',
                )


def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse('posts:posts-detail'), args={'pk':post.id})
    form = PostCreateForm()
    return render(request, 'posts/post_creation.html', {'form':form})


def detail_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post':post})


