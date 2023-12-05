from rest_framework.response import Response
from rest_framework.decorators import api_view
import sys
import time

sys.path.append("/home/boucherd/genAI/ChronoTalk")

from llm import run_conversation

global llm_chain
global conv_iteration

@api_view(['POST'])
def postMessage(request):
    # Get characterName and message from the request data
    character_name = request.data.get('characterName', '')
    message = request.data.get('message', '')

    # Your processing logic here...
    conv_iteration += 1

    if conv_iteration > 5:
        response = llm_chain.predict(user_input= message + "\nCreate another future based on this choice. Imagine what would be the major events in the following years by citing dates. At the end of your response, create a new dilemma and ask for 4 options for me to choose in the form of a list")
        #response = "e"
    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': "ça va tu coco, la vie dans le tieqs quoi",
        # Add any other data you want to include in the response
    }
    return Response(response_data)

@api_view(['GET'])
def getFirstMessage(request):
    character_name = request.query_params.get('characterName', '')

    # Instanciation of the model chain
    print("Loading the model")
    llm_chain = run_conversation.create_chain(character_name)

    prefix = "Start the conversation with respect to what I said before."
    
    message = llm_chain.predict(user_input=prefix)
    #message ="e"
    conv_iteration = 1

    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': message,
    }
    return Response(response_data)