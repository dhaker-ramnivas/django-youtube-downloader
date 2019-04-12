
from rest_framework import serializers


class FileNameCheck(serializers.Serializer):
    # In Get API check song name exist or not
    youtube_video_id = serializers.CharField(required=True,
                                            # error_messages={"error":"Please Enter Song Name Which You Want"}
                                            )


class CheckRequestSerializer(serializers.Serializer):
    # In Get API check song name exist or not
    task_id = serializers.CharField(required=True,
                                            # error_messages={"error":"Please Enter Song Name Which You Want"}
                                            )