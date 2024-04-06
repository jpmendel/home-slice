from datetime import datetime
from zoneinfo import ZoneInfo
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    content = models.TextField(max_length=1024)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # pylint: disable=no-member
        date_string = self.created_at.strftime("%Y-%m-%dT%H:%M:%S")
        return f"{self.id}-{self.author_name()}-{date_string}"

    def author_name(self):
        return self.author.username if self.author is not None else "user"

    def created_at_string(self):
        tz = ZoneInfo("America/New_York")
        # pylint: disable=no-member
        if self.created_at.date() == datetime.today().date():
            return f"at {self.created_at.astimezone(tz).strftime("%-I:%M %p")}"
        return f"on {self.created_at.astimezone(tz).strftime("%m/%d/%y")}"
