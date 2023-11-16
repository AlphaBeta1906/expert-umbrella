from django.contrib import admin
from .models import User,UserBan,LoginImage

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "groups",
        "account_confirmed",
        "is_staff",
        "is_active",
    )
    search_fields = ("username", "email", "id")
    readonly_fields = (
        "username",
        "email",
        "profile",
        "allow_nsfw",
        "show_liked_post",
    )
    list_filter = ("groups", "is_staff", "is_superuser")
    list_editable = ("is_staff", "groups", "account_confirmed", "is_active")

class UserBanAdmin(admin.ModelAdmin):
    list_display = ("id","user","ban_period","ban_category","ban_created","timestamp")
    search_fields = ("user",)
    readonly_fields = ("timestamp",)
    autocomplete_fields = ("user",)
    
    def has_change_permission(self, request, obj=None):
        return False
    
class LoginImageAdmin(admin.ModelAdmin):
    list_display = ("id","image_url","creator")

admin.site.register(User, UserAdmin)
admin.site.register(UserBan,UserBanAdmin)
admin.site.register(LoginImage,LoginImageAdmin)