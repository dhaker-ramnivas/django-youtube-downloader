import csv
import os
import coreapi
import logging
import coreschema
import sys
import sys
import json
sys.path.append(os.path.abspath(os.path.pardir))

from rest_framework.response import Response

logger = logging.getLogger(__name__)

from rest_framework import generics, status
from .models import UserSongDownloadTrack
from celery.result import AsyncResult
from celery import shared_task,current_task

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

from .serializers import FileNameCheck,CheckRequestSerializer
from rest_framework.schemas import AutoSchema

BASE_DIR = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])

from celery import result, Celery

app = Celery(backend='redis://')


class SongRequest(generics.GenericAPIView):
    """
    in this get API, user request a song by giving a name.
    If song is in local store then Id is return to user
    Else will return a temp id and download the song in background.
        when song will available then user can download the song
    """
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "youtube_video_id",
            required=True,
            location="query",
            schema=coreschema.String(),
            description="",
        ),
    ])

    @shared_task
    def downloadVideo(youtube_video_id):
        try:
            from pytube import YouTube
            from pytube.exceptions import VideoUnavailable

            yt = YouTube('https://www.youtube.com/watch?v={}'.format(youtube_video_id))
            logger.info(msg="downloading the data")

            yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download()


        except VideoUnavailable:
            logger.info(msg="Video not available by this id")
            return {"error ": "Video not available by this id"}



    def get(self,request, format=None):
        serializer = FileNameCheck(data=request.GET)
        if serializer.is_valid():
            x = self.downloadVideo.delay(request.GET.get('youtube_video_id'))

            if x.task_id:
                UserSongDownloadTrack.objects.create(
                    youtube_video_id = request.GET.get('youtube_video_id'),
                    task_id = x.task_id,
                    status  = x.state
                ).save()

            return Response({'error':False,
                             'message':"Video Started downloading",
                            'task_id':x.task_id
                             }, status=201)

        logger.error(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


def CheckDownloadIsInProcess(request):
    from celery import result, Celery

    app = Celery(backend='redis://')
    result = AsyncResult(request.data.get('task_id'), app=app)

    from .signals import chech_status
    chech_status.send_robust(sender= None,status = result.status,task_id = request.data.get('task_id'))

    return result


class CheckRequest(generics.GenericAPIView):
    """
    In this API user can check status of task by giving a task_id
    """
    serializer_class = CheckRequestSerializer

    def post(self,request):

        result = CheckDownloadIsInProcess(request)

        if not result:
            return Response(json.dumps({
                "error":"celery id not present"
            }), content_type='application/json')
        else:
            return Response(json.dumps({
                'state': result.state,
                'status': result.status,
                'result': result.result
            }), content_type='application/json')



class StopRequest(generics.GenericAPIView):
    """
    provide {"task_id":"celery_id "} in post API
    """
    serializer_class = CheckRequestSerializer

    def post(self,request):
        result = CheckDownloadIsInProcess(request) #check that task is done or not

        if result and result.status =='SUCCESS':
            return Response(json.dumps({
                'message':"Task Done Successfully" # not allowed to change status task, it is completed now
            }), content_type='application/json')


        from celery.contrib.abortable import AbortableAsyncResult

        abortable_task = AbortableAsyncResult(request.data.get('task_id'))
        abortable_task.abort()

        return  Response(json.dumps({
                'message':"Task Abort Done Successfully"
            }), content_type='application/json')

