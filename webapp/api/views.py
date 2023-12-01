from rest_framework.response import Response
from rest_framework.decorators import api_view

import time

@api_view(['POST'])
def postMessage(request):
    msg = request.data
    time.sleep(1)
    return Response(msg)