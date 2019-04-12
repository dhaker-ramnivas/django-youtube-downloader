from django.db import models
from django.dispatch import receiver

from .signals import chech_status
# Create your models here.

class UserSongDownloadTrack(models.Model):

   youtube_video_id = models.CharField(max_length = 100)
   status = models.CharField(max_length = 50)
   name = models.CharField(max_length = 50)
   task_id = models.CharField(max_length=100)

   class Meta:
      db_table = "user_song_download_track"


   @receiver(chech_status)
   def checkStatus(sender,status,task_id,**kwargs):
      print(status,"EEEEEE",type(status))
      if status:
         user_tack = UserSongDownloadTrack.objects.get(task_id = task_id)
         user_tack.status = status
         user_tack.save()