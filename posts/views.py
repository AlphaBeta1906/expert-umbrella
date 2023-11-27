from django.shortcuts import render, redirect, get_object_or_404
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from markdown import markdown
from bleach import clean
from reversion import create_revision,set_user,set_comment
from reversion.models import Version
from application.decorators import not_baned, active_required
from .models import Post, Tag, GroupPost, CommentPost
from .forms import (
    PostForm,
    ReportPostForm,
    GroupPostForm,
    EditGroupPostForm,
    SearchForm,
    CommentPostForm,
    ReportCommentPostForm,
)

# Create your views here.


class PostGroup:
    def __init__(self, group_post: list, current_post: Post):
        self.group_post: [Post] = group_post
        self.current_post: Post = current_post
        self.group_post_dict = (
            {_index: post for _index, post in enumerate(group_post)}
            if group_post
            else None
        )

    def get_next(self):
        """get next post in list after current post"""
        if not self.current_post.group:
            return None

        print(self.group_post_dict)

        for index, post in self.group_post_dict.items():
            if self.current_post == post:
                if index >= 0 and index < len(self.group_post_dict) - 1:
                    return self.group_post_dict[index + 1]
                break
        return None

    def __str__(self):
        return f"previous post {self.get_previous()}, next post {self.get_next()}  "

    def get_previous(self):
        """get previous post in list before current post"""
        if not self.current_post.group:
            return None

        for index, post in self.group_post_dict.items():
            if self.current_post == post:
                if index > 0 and index < len(self.group_post_dict) + 1:
                    return self.group_post_dict[index - 1]
                break
        return None

@not_baned
def index(request: HttpRequest):
    form = SearchForm()
    posts = Post.objects.filter(is_draft=False).all()

    page = request.GET.get("page", 1)
    query = request.GET.get("title", None)
    complete = request.GET.get("complete", None)

    if query:
        posts = posts.filter(title__contains=query).all()
    
    if complete:
        posts = posts.filter(is_complete=True).all()
        

    paginator = Paginator(posts, settings.ITEM_PER_PAGE)
    page_obj = paginator.get_page(page)

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["title"]
            return redirect("post:index", query=query)

    return render(
        request,
        "index.html",
        {
            "title": "Project shiorium|",
            "form": form,
            "is_posts": True,
            "search_placeholder": "Search post title",
            "posts": page_obj,
            "page": page_obj,
        },
    )

@not_baned
def read_post(request: HttpRequest, id, title):
    post = get_object_or_404(Post, id=id)
    versions = Version.objects.get_for_object(post)
    print(versions)

    if not request.user == post.author and post.is_draft:
        return HttpResponseNotFound()

    # post.content = markdown(post.content)

    group = post.group
    group_post = (
        Post.objects.filter(is_draft=False, group=group)
        .order_by("chapter_id")
        .all()
        if group
        else None
    )

    # posts_by_admin = Post.objects.filter(author=post.author,is_draft=False).all()

    if request.user == post.author and group_post:
        group_post = (
            Post.objects.filter(group=group).order_by("chapter_id").all()
        )
        # posts_by_admin = Post.objects.filter(author=post.author,is_draft=False).order_by("id").all()

    post_group = PostGroup(group_post, post)
    next_post = post_group.get_next()
    previous_post = post_group.get_previous()

    return render(
        request,
        "read.html",
        {
            "title": post.title,
            "post": post,
            "read_post": True,
            "next_post": next_post,
            "previous_post": previous_post,
            "group": group,
            "group_post": group_post,
        },
    )


@login_required
@active_required
@not_baned
def create_post(request: HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.content = clean(
                post.content,
                tags=settings.ALLOWED_HTML_TAGS,
                attributes=settings.ALLOWED_HTML_ATTRIBUTES,
                css_sanitizer=settings.CSS_SANITIZER,
                protocols=["data"],
            )

            if (
                post.group
                and Post.objects.filter(
                    chapter_id=post.chapter_id, group=post.group
                ).exists()
            ):
                post.chapter_id = (
                    Post.objects.filter(group=post.group).last().chapter_id + 1
                )
            else:
                post.chapter_id = 1
            with create_revision():
                post.save()
                form.save_m2m()
                
                set_user(request.user)
                set_comment("initial save")

            return redirect("post:index")

    form = PostForm()
    form.fields["group"].queryset = GroupPost.objects.filter(
        owner=request.user
    ).all()
    return render(
        request, "create.html", {"title": "Create post", "form": form}
    )


@login_required
@active_required
@not_baned
def edit_post(request: HttpRequest, id, title):
    post = Post.objects.filter(id=id).first()

    if not request.user == post.author:
        return HttpResponseNotFound()

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.content = clean(
                post.content,
                tags=settings.ALLOWED_HTML_TAGS,
                attributes=settings.ALLOWED_HTML_ATTRIBUTES,
                css_sanitizer=settings.CSS_SANITIZER,
                protocols=["data"],
            )

            if (
                post.group
                and Post.objects.filter(
                    chapter_id=post.chapter_id, group=post.group
                ).exists()
            ):
                post.chapter_id = (
                    Post.objects.filter(group=post.group).last().chapter_id + 1
                )
            else:
                post.chapter_id = 1
            post.save()
            form.save_m2m()
            return redirect("post:index")

    form = PostForm(instance=post)
    form.fields["group"].queryset = GroupPost.objects.filter(
        owner=request.user
    ).all()
    return render(
        request,
        "create.html",
        {
            "title": "Edit post",
            "form": form,
            "is_draft": post.is_draft,
            "content": post.content,
            "edit": True,
        },
    )


@login_required
@active_required
@not_baned
def delete_post(request: HttpRequest, id, title):
    posts = get_object_or_404(Post, id=id)
    if posts.author == request.user:
        posts.delete()
        return redirect("post:index")
    else:
        return HttpResponseNotFound()


@login_required
@require_POST
@not_baned
def like_post(request: HttpRequest, id, title):
    post = get_object_or_404(Post, id=id)
    if not request.user in post.likes.all():
        post.likes.add(request.user)
        # if request.user != post.author:
        #     notify.send(request.user,recipient=post.author,verb="Someone like your post",target=post)
        return JsonResponse({"msg": f"{request.user} like {post}"})
    else:
        post.likes.remove(request.user)
        return JsonResponse({"msg": f"{request.user} unlike {post}"})


@login_required
@active_required
@not_baned
def report_post(request: HttpRequest, id, title):
    post = get_object_or_404(Post, id=id)
    form = ReportPostForm()

    if request.method == "POST":
        form = ReportPostForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.post = post
            report.save()
            messages.info(request, "Reporting post success")
            return redirect("post:index")

    return render(
        request,
        "report.html",
        {"title": "Report post", "form": form, "post": post},
    )

@not_baned
def tag_post(request: HttpRequest, slug):
    form = SearchForm()

    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(is_draft=False, tag=tag).all()

    page = request.GET.get("page", 1)
    query = request.GET.get("title", None)
    complete = request.GET.get("complete",None)

    if query:
        posts = posts.filter(title__contains=query).all()
    
    if complete:
        posts = posts.filter(is_complete=True).all()
    

    paginator = Paginator(posts, settings.ITEM_PER_PAGE)
    page_obj = paginator.get_page(page)

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["title"]
            return redirect("post:index", query=query)

    return render(
        request,
        "index.html",
        {
            "title": f"Tag: {tag}",
            "form": form,
            "is_posts": True,
            "search_placeholder": "Search post in this tag",
            "posts": page_obj,
            "page": page_obj,
            "tag": tag,
        },
    )


@login_required
@active_required
@not_baned
def create_group(request: HttpRequest):
    form = GroupPostForm()
    if request.method == "POST":
        form = GroupPostForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.owner = request.user
            group.save()
            return redirect("post:group")
    return render(
        request, "group.html", {"title": "Create new group post", "form": form}
    )

@not_baned
def group_post(request: HttpRequest, id, title):
    """ "a page to display list of posts in a group"""
    group = get_object_or_404(GroupPost, id=id)
    posts = (
        Post.objects.filter(is_draft=False, group=group)
        .order_by("chapter_id")
        .all()
    )
    draft_post = 0

    if request.user == group.owner:
        posts = Post.objects.filter(group=group).all()

    paginator = Paginator(posts, settings.ITEM_PER_PAGE)
    page = request.GET.get("page", 1)

    page_obj = paginator.get_page(page)
    return render(
        request,
        "index.html",
        {
            "title": f"Group: {group}",
            "posts": page_obj,
            "page": page_obj,
            "group": group,
            "is_posts": True,
        },
    )


@login_required
@active_required
@not_baned
def edit_group(request: HttpRequest, id, title):
    group = get_object_or_404(GroupPost, id=id)

    if not request.user == group.owner:
        return HttpResponseNotFound()

    form = GroupPostForm(instance=group)

    if request.method == "POST":
        form = GroupPostForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect("post:group")
    # form.fields["posts"].queryset = Post.objects.filter(author=request.user).all()

    return render(
        request,
        "group.html",
        {
            "title": f"Edit group post {group.title} ",
            "edit": True,
            "form": form,
        },
    )

@not_baned
def group_index(request: HttpRequest):
    """a page to display list of groups"""
    form = SearchForm()

    groups = GroupPost.objects.all()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            return redirect("post:group", query=title)

    page = request.GET.get("page", 1)
    query = request.GET.get("query", None)

    if query:
        groups = groups.filter(name__contains=title).all()

    paginator = Paginator(groups, settings.ITEM_PER_PAGE)
    page_obj = paginator.get_page(page)

    return render(
        request,
        "index.html",
        {
            "title": "Post groups",
            "is_group": True,
            "search_placeholder": "Search post group",
            "form": form,
            "groups": page_obj,
            "page": page_obj,
        },
    )

@login_required
@active_required
@not_baned
def group_delete(request: HttpRequest, id, title):
    group = get_object_or_404(GroupPost, id=id)

    if group.owner == request.user:
        group.delete()
        return redirect("post:group")
    else:
        return HttpResponseForbidden()

@login_required
@require_POST
@not_baned
def follow_group(request: HttpRequest,id):
    group = get_object_or_404(GroupPost,id=id)
    
    if request.user == group.owner:
        return JsonResponse({"msg": "you can't follow your own group"},status=403)

    if not request.user in group.followers.all():
        group.followers.add(request.user)
        return JsonResponse({"msg": f"{request.user} follow {group}"})
    else:
        group.followers.remove(request.user)
        return JsonResponse({"msg": f"{request.user} unfollow {group}"})

@not_baned
def comment_post(request: HttpRequest, id, title):
    post = get_object_or_404(Post, id=id)

    if not request.user == post.author and post.is_draft:
        return HttpResponseNotFound()

    comments = CommentPost.objects.filter(post=post).all()
    comments_count = comments.count()

    form = CommentPostForm()

    if request.method == "POST":
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("post:comments", id=id, title=slugify(post.title))

    return render(
        request,
        "comment.html",
        {
            "title": f"{post.title} comments",
            "post": post,
            "comments_count": comments_count,
            "comments": comments,
            "form": form,
        },
    )

@login_required
@active_required
@not_baned
def report_comment(request: HttpRequest, id):
    _comment = get_object_or_404(CommentPost, id=id)
    form = ReportCommentPostForm()
    
    post_id = request.GET.get("post_id",None)
    post_title = request.GET.get("post_title",None)
    
    if request.method == "POST":
        form = ReportCommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.comment = _comment
            comment.save()
            messages.info(request, "Reporting comment success")
            
            if not post_id or not post_title:
                return redirect("post:index")
            return redirect("post:comments", id=post_id, title=slugify(post_title))

    return render(
        request,
        "report.html",
        {
            "title": "Report comment",
            "form": form,
            "is_commnet": True,
            "comment": _comment,
        },
    )

@not_baned
def tag_index(request: HttpRequest):
    tags = Tag.objects.all()

    return render(request, "tags.html", {"title": "Tags", "tags": tags})
