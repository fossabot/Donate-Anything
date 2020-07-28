from django.conf import settings
from django.db import models


THREAD_TYPE_CHOICES = (
    (0, "General Message"),
    (1, "Organization Application"),  # # 80% majority, vote. Staff or verified merge.
    (2, "Business Application"),  # 80% majority vote. Staff or verified merge.
    (3, "Entity Suggested Edit"),  # 80% majority vote. Staff or verified merge.
    (4, "Adding/Removing Items"),  # 5/10 votes, Doesn't require staff approval
)


class Thread(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(choices=THREAD_TYPE_CHOICES)
    views = models.BigIntegerField(default=0)
    # They will always show in the forum, but this just makes sure a merge happened
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Message(models.Model):
    """A message in a thread is a simple message. Nothing special.
    """

    id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)