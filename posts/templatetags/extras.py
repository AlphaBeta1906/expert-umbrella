from django import template
from ..models import Post, GroupPost
from users.models import LoginImage

register = template.Library()


@register.simple_tag
def get_draft_post(post_group: GroupPost, current_user):
    if current_user == post_group.owner:
        return Post.objects.filter(group=post_group.id, is_draft=True).count()
    return 0

@register.simple_tag
def get_login_image():
    return LoginImage.objects.order_by("?").first()