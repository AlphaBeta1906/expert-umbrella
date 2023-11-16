from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from colorfield.fields import ColorField

# Create your models here.

User = get_user_model()


def get_class():
    classes = open("./posts/tag_css_class.txt")
    return [(_class.strip(), _class.strip()) for _class in classes.readlines()]


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.TextField(max_length=150)
    background_color = ColorField(default="#0088ffd0")

    def __str__(self):
        return self.name

    def post_count(self):
        return Post.objects.filter(tag=self.id).count()


class GroupPost(models.Model):
    title = models.CharField(max_length=150, null=False, blank=False)
    description = models.TextField(blank=False, max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    followers = models.ManyToManyField(
        User, null=True, default=True, related_name="follower_set"
    )

    # posts = models.ManyToManyField(Post,related_name="group_post_set",through="PostSeries")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def post_count(self):
        group = GroupPost.objects.filter(id=self.id).first()
        return Post.objects.filter(is_draft=False, group=self.id).count()


class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    content = models.TextField(
        help_text="This site are using markdown to writing content, You can find the guide at <a target='_blank' href='https://www.markdownguide.org/cheat-sheet/'>here</a> ",
        null=True,
    )
    # content = models.OneToOneField(Document,on_delete=models.CASCADE,null=True)
    summary = models.TextField(
        null=True,
        blank=False,
        default="No summary",
        max_length=250,
        verbose_name="Post summary",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    date_published = models.DateTimeField(null=True)
    tag = models.ManyToManyField(
        Tag, null=True, related_name="post_tags_set", blank=False
    )
    is_draft = models.BooleanField(
        default=True, verbose_name="Set your post as draft"
    )
    is_complete = models.BooleanField(
        default=False, verbose_name="Set your post as complete"
    )
    cover_image = models.URLField(null=True, blank=True)
    likes = models.ManyToManyField(
        User, null=True, related_name="user_likes_set"
    )
    is_hide = models.BooleanField(default=False, verbose_name="Hide post")
    group = models.ForeignKey(
        GroupPost,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        blank=True,
    )
    chapter_id = models.PositiveIntegerField(blank=True, default=1)
    is_nsfw = models.BooleanField(
        default=False, verbose_name="Flag your post as an nsfw post"
    )

    def save(self, *args, **kwargs):

        if self.is_draft and not self.date_published:
            self.date_published = timezone.now()

        if not self.is_draft and not self.date_published:
            self.date_published = timezone.now()

        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date_published", "-date_created", "-date_updated"]

    def report_count(self):
        return ReportPost.objects.filter(post=self.id, is_read=True).count()

    def comment_count(self):
        return CommentPost.objects.filter(post=self.id).count()


class PostSeries(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    post_order = models.IntegerField(default=1)


class CommentPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False)
    content = models.TextField(
        max_length=250, blank=False, null=False, verbose_name="Your comment"
    )
    date_created = models.DateTimeField(auto_now_add=True, auto_created=True)
    likes = models.ManyToManyField(
        User, null=True, related_name="comment_likes"
    )

    def __str__(self):
        return f"{self.author.get_username()} comment at {self.date_created} "

    def report_count(self):
        return ReportCommentPost.objects.filter(
            comment=self.id, is_read=True
        ).count()


class BaseReportModel(models.Model):
    REPORT_NAME = [
        ("Unappropriate content", "Unappropriate content"),
        ("Another report", "Another report"),
    ]

    reason = models.CharField(
        max_length=50,
        choices=REPORT_NAME,
        null=True,
        blank=False,
        verbose_name="Report reason",
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        blank=False, default="", verbose_name="Report description"
    )
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ReportPost(BaseReportModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"report id: {self.pk} "


class ReportCommentPost(BaseReportModel):
    comment = models.ForeignKey(CommentPost, on_delete=models.CASCADE)

    def __str__(self):
        return f"report id: {self.pk} "
