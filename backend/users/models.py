from __future__ import annotations
from djongo import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
import datetime
import hashlib
import uuid
from typing import Any



import user_agents
from django.conf import settings
from django.http import HttpRequest
from django.utils import timezone
from django.utils.translation import gettext_lazy as _lazy

from .settings import REQUEST_CONTEXT_ENCODER, REQUEST_CONTEXT_EXTRACTOR



def parse_remote_addr(request: HttpRequest) -> str:
    """Extract client IP from request."""
    x_forwarded_for = request.headers.get("X-Forwarded-For", "")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    return request.META.get("REMOTE_ADDR", "")


def parse_ua_string(request: HttpRequest) -> str:
    """Extract client user-agent from request."""
    return request.headers.get("User-Agent", "")



# Create your models here.
class Articles(models.Model):
    article_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    domain = models.CharField(max_length=100)

    class Meta:
        abstract = True
        
class Associations(models.Model):
    user_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True
        

class User(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length = 254)
    occupation = models.CharField(max_length=150,null=True)
    username = models.CharField(max_length=25)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="")
    phoneno = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    location = models.CharField(max_length=100,null=True)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    gender = models.CharField(choices=[('Male','Male'),('Female','Female'),('Others','Others')], default="Male", max_length=6)
    associations = models.EmbeddedField(
        model_container=Associations,null=True, blank=True
    )
    active = models.BooleanField(default=True)
    published = models.EmbeddedField(
        model_container=Articles,null=True, blank=True
    )
    liked_article = models.EmbeddedField(
        model_container=Articles, null=True, blank=True
    )
    headline = models.CharField(max_length=255, null=True, blank=True)    
    objects = models.DjongoManager()
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        instance.profile.save()
        
        
class UserVisit(models.Model):
    """
    Record of a user visiting the site on a given day.
    This is used for tracking and reporting - knowing the volume of visitors
    to the site, and being able to report on someone's interaction with the site.
    We record minimal info required to identify user sessions, plus changes in
    IP and device. This is useful in identifying suspicious activity (multiple
    logins from different locations).
    Also helpful in identifying support issues (as getting useful browser data
    out of users can be very difficult over live chat).
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_visits", on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(
        help_text="The time at which the first visit of the day was recorded",
        default=timezone.now,
    )
    session_key = models.CharField(help_text="Django session identifier", max_length=40)
    remote_addr = models.CharField(
        help_text=(
            "Client IP address (from X-Forwarded-For HTTP header, "
            "or REMOTE_ADDR request property)"
        ),
        max_length=100,
        blank=True,
    )
    ua_string = models.TextField(
        "User agent (raw)", help_text="Client User-Agent HTTP header", blank=True,
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    hash = models.CharField(
        max_length=32,
        help_text="MD5 hash generated from request properties",
        unique=True,
    )
    created_at = models.DateTimeField(
        help_text="The time at which the database record was created (!=timestamp)",
        auto_now_add=True,
    )

    class UserVisitManager(models.DjongoManager):
        """Custom model manager for UserVisit objects."""

        def build(self, request: HttpRequest, timestamp: datetime.datetime):
            """Build a new UserVisit object from a request, without saving it."""
            uv = UserVisit(
                user=request.user,
                timestamp=timestamp,
                session_key=request.session.session_key,
                remote_addr=parse_remote_addr(request),
                ua_string=parse_ua_string(request),
                #context=REQUEST_CONTEXT_EXTRACTOR(request),
            )
            uv.hash = uv.md5().hexdigest()
            data = uv.make_json_value()
            return data,uv.hash
    
    objects = UserVisitManager()

    class Meta:
        get_latest_by = "timestamp"

    def __str__(self) -> str:
        return f"{self.user} visited the site on {self.timestamp}"

    def __repr__(self) -> str:
        return f"<UserVisit id={self.id} user_id={self.user_id} date='{self.date}'>"

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Set hash property and save object."""
        self.hash = self.md5().hexdigest()
        super().save(*args, **kwargs)
        
    def make_json_value(self):
        return {'user':str(self.user),'timestamp':self.timestamp,'session_key':self.session_key,
                'remote_addr':self.remote_addr,'ua_string':self.ua_string,'hash':self.hash,
                'uuid':self.uuid,'created_at':self.created_at,'user_id':0,
                'id':uuid.uuid4().int & (1<<8)-1}

    @property
    def user_agent(self) -> user_agents.parsers.UserAgent:
        """Return UserAgent object from the raw user_agent string."""
        return user_agents.parsers.parse(self.ua_string)

    @property
    def date(self) -> datetime.date:
        """Extract the date of the visit from the timestamp."""
        return self.timestamp.date()

    # see https://github.com/python/typeshed/issues/2928 re. return type
    def md5(self) -> hashlib._Hash:
        """Generate MD5 hash used to identify duplicate visits."""
        h = hashlib.md5(str(self.user.id).encode())  # noqa: S303
        h.update(self.date.isoformat().encode())
        h.update(self.session_key.encode())
        h.update(self.remote_addr.encode())
        h.update(self.ua_string.encode())
        return h