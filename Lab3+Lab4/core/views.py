from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from .forms import PostForm, BlockListForm
from .models import BlogUser, Post, BlockList

# Create your views here.


def posts(request: HttpRequest):
    # check if the user is logged in if not redirect to admin
    if not request.user.is_authenticated:
        return redirect("admin:index")
    blocked_by = BlockList.objects.filter(
        blocked_user__user=request.user
    ).values_list("user", flat=True)
    curated_posts = Post.objects.exclude(author__user__in=blocked_by).exclude(author__user=request.user)
    # exclude the posts from the current user
    print(curated_posts)
    context = dict()
    context["posts"] = curated_posts

    return render(request, "index.html", context=context)


def profile(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("admin:index")
    user = BlogUser.objects.get(user=request.user)
    visible_posts = Post.objects.filter(author=user)
    context = dict()
    context["posts"] = visible_posts
    context["user"] = user

    return render(request, "profile.html", context=context)


def add_post(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("admin:index")
    context = dict()
    context["form"] = PostForm
    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = BlogUser.objects.get(user=request.user)
            post.save()

            return redirect("posts")

    return render(request, "add.html", context=context)


def blocked_users(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("admin:index")

    if request.method == "POST":
        form = BlockListForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            block_list = form.save(commit=False)
            block_list.user = BlogUser.objects.get(user=request.user)
            block_list.save()
            return redirect("blocked")
    else:
        context = dict()
        context["form"] = BlockListForm
        block_list = BlockList.objects.filter(user__user=request.user)
        blocked = BlogUser.objects.filter(id__in=block_list.values_list("blocked_user", flat=True))
        context["blocked"] = blocked
        return render(request, "blocked.html", context=context)
