from django import template
from ..models import Post, GroupPost

register = template.Library()


@register.simple_tag
def get_draft_post(post_group: GroupPost, current_user):
    if current_user == post_group.owner:
        return Post.objects.filter(group=post_group.id, is_draft=True).count()
    return 0
