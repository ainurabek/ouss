from shutil import disk_usage

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class MemoryInfoAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        total, used, free = disk_usage("/")
        data = {
            "total": round(total/1000000000, 2),
            "used": round(used/1000000000, 2),
            "free": round(free/1000000000, 2)
        }
        return Response(data, status=status.HTTP_200_OK)
