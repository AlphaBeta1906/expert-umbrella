from django import forms
from django.forms import ModelForm
from django_select2 import forms as SelectForm
from .models import (
    Post,
    ReportPost,
    GroupPost,
    Tag,
    CommentPost,
    ReportCommentPost,
)


class TagWidget(SelectForm.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = (
            "title",
            "tag",
            "cover_image",
            "summary",
            "content",
            "group",
            "chapter_id",
            "is_nsfw",
            "is_complete",
            "is_draft",
        )
        widgets = {"tag": TagWidget}


class ReportPostForm(ModelForm):
    class Meta:
        model = ReportPost
        fields = ("reason", "description")


class GroupPostForm(ModelForm):
    class Meta:
        model = GroupPost
        fields = ("title", "description")


class EditGroupPostForm(ModelForm):
    class Meta:
        model = GroupPost
        fields = ("title", "description")


class SearchForm(forms.Form):
    title = forms.CharField(max_length=50, required=True)
    tag = forms.ModelChoiceField(queryset=Tag.objects.all(), required=False)
    complete = forms.BooleanField(initial=True, required=False)


class CommentPostForm(ModelForm):
    class Meta:
        model = CommentPost
        fields = ("content",)


class ReportCommentPostForm(ModelForm):
    class Meta:
        model = ReportCommentPost
        fields = ("reason", "description")

class PostRevisionForm(forms.Form):
    revisions = forms.ModelChoiceField(queryset=None)
