from django.shortcuts import render
from django.utils import timezone
from functools import wraps
from users.models import User,UserBan


def active_required(function):
    """
    Decorator check if user account alrady confirmed
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user: User = request.user
        print(user.is_active)
        if (
            not user.account_confirmed
            and user.is_authenticated
            and not user.is_superuser
        ):
            return render(request, "unconfirmed.html")
        else:
            return function(request, *args, **kwargs)

    return wrap


def not_baned(function):
    """
    Decorator to check if user is in baned period or not
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            user: UserBan = UserBan.objects.filter(user=request.user).order_by("-ban_created").first()
            # print(timezone.now())
            # print(user.timestamp)
            if user:
                if timezone.now() < user.timestamp:
                    return render(request, "unconfirmed.html", {"title": "Account baned","is_ban": True,"ban": user})

        return function(request, *args, **kwargs)

    return wrap
