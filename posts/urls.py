from django.urls import path
from . import views

app_name = "post"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/create/", views.create_post, name="create"),
    path("post/edit/<int:id>/<str:title>", views.edit_post, name="edit"),
    path("post/read/<int:id>/<str:title>", views.read_post, name="read"),
    path("post/delete/<int:id>/<str:title>", views.delete_post, name="delete"),
    path("post/like/<int:id>/<str:title>", views.like_post, name="like"),
    path("post/report/<int:id>/<str:title>", views.report_post, name="report"),
    path("post/revision/", views.edit_revision, name="revision"),
    path("tag/<slug:slug>", views.tag_post, name="tag"),
    path("tag/", views.tag_index, name="tagindex"),
    path("group/", views.group_index, name="group"),
    path("group/create/", views.create_group, name="groupcreate"),
    path("group/<int:id>/<str:title>", views.group_post, name="grouppost"),
    path("group/follow/<int:id>",views.follow_group,name="likegroup"),
    path(
        "group/edit/<int:id>/<str:title>", views.edit_group, name="groupedit"
    ),
    path(
        "group/delete/<int:id>/<str:title>",
        views.group_delete,
        name="groupdelete",
    ),
    path("comments/<int:id>/<str:title>", views.comment_post, name="comments"),
    path("comments/<int:id>", views.delete_comment, name="deletecomment"),
    path(
        "report/comment/<int:id>", views.report_comment, name="reportcomment"
    ),
    path("notification/", views.notifications_page, name="notification"),
    path("notification/read/<int:id>", views.mark_notification, name="readnotification"),
]
