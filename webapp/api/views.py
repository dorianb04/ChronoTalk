from rest_framework.response import Response
from rest_framework.decorators import api_view

import time

@api_view(['POST'])
def postMessage(request):
    # Get characterName and message from the request data
    character_name = request.data.get('characterName', '')
    message = request.data.get('message', '')

    # Your processing logic here...

    # Simulate some processing time (remove this in production)
    time.sleep(1)

    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': message,
        # Add any other data you want to include in the response
    }
    return Response(response_data)