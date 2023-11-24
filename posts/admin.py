from django.contrib import admin
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import get_template,render_to_string
from zipfile import ZipFile
from io import BytesIO
from .models import (
    Post,
    Tag,
    ReportPost,
    GroupPost,
    CommentPost,
    ReportCommentPost,
)

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "date_created",
        "date_updated",
        "date_published",
        "is_draft",
        "is_complete",
        "cover_image",
        "like_count",
        "report_count",
    )
    search_fields = ("title", "author")
    date_hierarchy = "date_created"
    list_filter = ("is_draft", "is_complete", "tag")
    readonly_fields = (
        "title",
        "author",
        "date_created",
        "chapter_id",
        "group",
        "date_published",
        "is_nsfw",
        "summary",
        "content",
        "is_draft",
        "is_complete",
        "cover_image",
        "tag",
        "likes",
        "report_count",
    )
    actions = ("export_html",)

    def has_add_permission(self, obj: Post = None):
        return False

    def report_count(self, obj: Post = None):
        if obj:
            return obj.report_count()

    def like_count(self, obj: Post = None):
        if obj:
            return len(obj.likes.all())
    
    @admin.action(description="Export to html")
    def export_html(self, request, queryset):
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for post in queryset:
                html_content = render_to_string("read.html",{"title": post.title,"post": post,},)
                zip_file.writestr(f"post_{post.id}.html", html_content)
        zip_buffer.seek(0)

        response = HttpResponse(zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="exported_data.zip"'
        return response
    

class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "background_color")
    readonly_fields = ("slug",)


class GroupPostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "post_count")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def post_count(self, obj: GroupPost = None):
        if obj:
            return obj.post_count()


class ReportPostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "reason", "is_read")
    readonly_fields = ("author", "reason", "post", "description")
    list_editable = ("is_read",)

    def has_add_permission(self, request):
        return False


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "report_count")
    search_fields = ("id", "author", "post")

    def has_add_permission(self, request):
        return False

    def report_count(self, obj: CommentPost = None):
        if obj:
            return obj.report_count()


class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "comment", "reason", "is_read")
    readonly_fields = ("author", "reason", "comment", "description")
    list_editable = ("is_read",)

    def has_add_permission(self, request):
        return False


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ReportPost, ReportPostAdmin)
admin.site.register(GroupPost, GroupPostAdmin)
admin.site.register(CommentPost, CommentAdmin)
admin.site.register(ReportCommentPost, ReportCommentAdmin)
