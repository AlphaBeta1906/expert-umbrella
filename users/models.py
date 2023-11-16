from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils import timezone
from datetime import timedelta


class Role(models.Model):
    role_name = models.CharField(max_length=15, null=False)
    description = models.TextField(
        max_length=100, default="description of the role"
    )

    def __str__(self):
        return self.role_name


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=50)
    groups = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="role",
    )
    profile = models.TextField(
        max_length=250,
        help_text="Tell about yourself(max: 250 characthers)",
        verbose_name="User profile",
        null=True,
        blank=True,
    )
    ban = models.BooleanField(default=False)
    show_liked_post = models.BooleanField(
        default=False, verbose_name="Show your liked posts publicly"
    )
    allow_nsfw = models.BooleanField(
        default=False, verbose_name="Allow nsfw posts"
    )
    account_confirmed = models.BooleanField(default=False,help_text="confirm user account")
    show_email = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.username

class UserBan(models.Model):
    BAN_PERIOD_CHOICES = (
        ("1m", "1 Minute"),
        ("5m", "5 Minutes"),
        ("1h", "1 Hour"),
        ("4h", "4 Hours"),
        ("24h", "24 Hours"),
        ("7d", "7 Days"),
        ("30d", "30 Days"),
        ("perma", "Permanent"),
    )
    BAN_CATEGORY_CHOICES = (
        ("SPAM", "Spamming"),
        ("ABUSE", "Abusive Behavior"),
        ("HARASSMENT", "Harassment"),
        ("THREATS", "Threats of Violence"),
        ("IMPERSONATION", "Impersonation"),
        ("COPYRIGHT_INFRINGEMENT", "Copyright Infringement"),
        ("CHEATING", "Cheating"),
        ("VIOLATING_TERMS_OF_SERVICE", "Violating Terms of Service"),
        ("OTHER", "Other"),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(null=False)
    description = models.TextField(null=False)
    ban_period = models.CharField(max_length=50,choices=BAN_PERIOD_CHOICES)
    ban_category = models.CharField(max_length=150,choices=BAN_CATEGORY_CHOICES)
    ban_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-ban_created"]

    def save(self,*args,**kwargs):
        BAN_PERIODS = {
            "1m": timedelta(minutes=1),
            "5m": timedelta(minutes=5),
            "1h": timedelta(hours=1),
            "4h": timedelta(hours=4),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7),
            "30d": timedelta(days=30),
            "perma": timedelta(days=999999999),
        }
        
        self.timestamp = timezone.now() + BAN_PERIODS[self.ban_period]
        
        super(UserBan, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user} ban"
    
class LoginImage(models.Model):
    image_url = models.URLField(help_text="twitter url to an image",null=False,blank=False)
    creator = models.CharField(max_length=50, null=False, blank=False)