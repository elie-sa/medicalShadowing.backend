from django.db import models

class RoomMember(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=1000)
    room_name = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    session_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    session_time = models.CharField(max_length=200)

    def __str__(self):
        return self.name
