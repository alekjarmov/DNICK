from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from .forms import PostForm, BlockListForm
from .models import BlogUser, Post, BlockList
# Create your views here.


def posts(request: HttpRequest):
    blocked_by = BlockList.objects.filter(
        blocked_user__user=request.user
    ).values_list("user", flat=True)
    curated_posts = Post.objects.exclude(author__user__in=blocked_by).exclude(author__user=request.user)
    # exclude the posts from the current user
    context = dict()
    context["posts"] = curated_posts

    return render(request, "index.html", context=context)


def profile(request: HttpRequest):
    pass
    # user = BlogUser.objects.get(user=request.user)
    # visible_posts = Post.objects.filter(user=user)
    #
    # return render(request, "profile.html", {"user": user, "posts": visible_posts})


def add_post(request: HttpRequest):
    pass
    # if request.method == "POST":
    #     form_data = PostForm(data=request.POST, files=request.FILES)
    #
    #     if form_data.is_valid():
    #         post = form_data.save(commit=False)
    #         post.user = BlogUser.objects.get(user=request.user)
    #         post.save()
    #
    #         return redirect("posts")
    #
    # return render(request, "add.html", {"form": PostForm})


def blocked_users(request: HttpRequest):
    pass
    # if request.method == "POST":
    #     form_data = BlockListForm(data=request.POST, files=request.FILES)
    #
    #     if form_data.is_valid():
    #         block = form_data.save(commit=False)
    #         block.blocker = BlogUser.objects.get(user=request.user)
    #         block.save()
    #
    #         return redirect("blocked")
    #
    # blocks = Block.objects.filter(blocker__user=request.user)
    # blocked_users = BlogUser.objects.filter(user__in=blocks.values_list("blocked__user", flat=True))
    #
    # return render(request, "blocked.html", {"form": BlockForm, "users": blocked_users})