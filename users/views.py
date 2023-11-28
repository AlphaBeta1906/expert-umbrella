from django.shortcuts import render, redirect, resolve_url, get_object_or_404
from django.http import HttpRequest
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login,authenticate
from django.core.paginator import Paginator
from bleach import clean
from application.decorators import not_baned,active_required
from posts.models import Post, GroupPost
from .models import User
from .forms import CreateUserForm as UserCreationForm, EditProfileForm

# Create your views here.


def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(resolve_url("user:login"))
    else:
        form = UserCreationForm()
    print(form.errors)
    return render(
        request, "registration/signup.html", {"form": form, "title": "Signup"}
    )

@login_required
@not_baned
def profile(request: HttpRequest, username):
    get_user = get_object_or_404(User, username=username)

    user = get_user_model()

    is_group = request.GET.get("is_group", False)
    liked_post = request.GET.get("liked_post", False)
    posts_mode = request.GET.get("posts", "all")
    page = request.GET.get("page", 1)

    posts_mode_dict = {
        "all": Post.objects.filter(author=get_user, is_complete=False),
        "complete": Post.objects.filter(author=get_user, is_complete=True),
        "draft": Post.objects.filter(author=get_user, is_draft=True),
    }

    posts = posts_mode_dict[posts_mode].filter(is_draft=False).all()

    if request.user == get_user:
        posts = posts_mode_dict[posts_mode].all()
        print(posts)
        
    paginator = Paginator(posts, settings.ITEM_PER_PAGE)
    page_obj = paginator.get_page(page)

    if is_group:
        groups = GroupPost.objects.filter(owner=get_user).all()
        paginator = Paginator(groups, settings.ITEM_PER_PAGE)
        page_obj = paginator.get_page(page)
        return render(
            request,
            "user.html",
            {
                "title": "My profile"
                if get_user.username == request.user.username
                else f"Profile | {get_user.username}",
                "groups": groups,
                "get_user": get_user,
                "posts": page_obj,
                "page": page_obj,
                "is_group": is_group,
            },
        )

    if liked_post:
        posts = Post.objects.filter(likes=request.user).all()

        paginator = Paginator(posts, settings.ITEM_PER_PAGE)
        page_obj = paginator.get_page(page)

        return render(
            request,
            "user.html",
            {
                "title": "My profile"
                if get_user.username == request.user.username
                else f"Profile | {get_user.username}",
                "posts": page_obj,
                "page": page_obj,
                "get_user": get_user,
                "liked_post": True,
            },
        )

    return render(
        request,
        "user.html",
        {
            "title": "My profile"
            if get_user.username == request.user.username
            else f"Profile | {get_user.username}",
            "posts": page_obj,
            "page": page_obj,
            "get_user": get_user,
        },
    )


@login_required
@not_baned
def edit_profile(request: HttpRequest, username):
    get_user = get_object_or_404(User, username=username)
    form = EditProfileForm(instance=get_user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=get_user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.profile = clean(
                profile.profile,
                tags=settings.ALLOWED_HTML_TAGS,
                attributes=settings.ALLOWED_HTML_ATTRIBUTES,
                css_sanitizer=settings.CSS_SANITIZER,
            )
            profile.save()
            return redirect("user:profile", username=get_user.username)
    return render(
        request, "edit_profile.html", {"title": "Edit profile", "form": form}
    )
