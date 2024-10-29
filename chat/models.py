from django.db import models

# Create your models here.
class Message(models.Model):
    # room = models.ForeignKey('Room', related_name='messages', on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=255)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender}: {self.content} ({self.timestamp})"

# class Room(models.Model):
#     name = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)