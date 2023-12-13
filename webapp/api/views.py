from rest_framework.response import Response
from rest_framework.decorators import api_view
import sys
import time

sys.path.append("/home/boucherd/genAI/ChronoTalk")

from llm import run_conversation

# Initialization of the global variables
llm_chain = None
conv_iteration = 0
isModelLoad = False

@api_view(['POST'])
def postMessage(request):
    global conv_iteration
    global llm_chain

    # Get characterName and message from the request data
    character_name = request.data.get('characterName', '')
    message = request.data.get('message', '')
    print(conv_iteration)
    # Your processing logic here...
    
    conv_user_input_conditioning = """
    \nCreate another future based on this choice. Imagine what would be the major events in the following years by citing dates. At the end of your response, create a new dilemma and ask for 4 options for me to choose in the form of a list like this:
        <br>1. Option 1
        <br>2. Option 2
        <br>3. Option 3
        <br>4. Option 4
    """

    end_user_input_conditioning = """
    \nThis is the end of our conversation. You then imagine what would be the major events in the following years and wrap up all of what we said in less than 100 words. Finish the conversation as an emperor."""
    
    if conv_iteration < 5:
        response = llm_chain.predict(user_input= message + conv_user_input_conditioning)
        conv_iteration += 1
    else:
        response = llm_chain.predict(user_input= message + end_user_input_conditioning)
    
    print(response)

    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': response.replace("\n", '<br>')[4:],
        # Add any other data you want to include in the response
    }
    return Response(response_data)

@api_view(['GET'])
def getFirstMessage(request):
    global conv_iteration
    global llm_chain

    character_name = request.query_params.get('characterName', '')

    

    prefix = """Start the conversation with respect to what I said before. You tell me about your history until the end of the french revolution. Then Create a new dilemma and generate 4 options for me to choose in the form of a list like this:
        <br>1. ...
        <br>2. ...
        <br>3. ...
        <br>4. ...
    """
    
    message = llm_chain.predict(user_input=prefix)
    #message ="e"
   
    conv_iteration = 1

    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': message,
    }
    return Response(response_data)



@api_view(['POST'])
def loadModel(request):
    global llm_chain
    global isModelLoad
    
    if isModelLoad:
        return Response({'Status': "Model already loaded"})
    
    else:
        # Instanciation of the model chain
        print("Loading the model")
        llm_chain = run_conversation.create_chain()
        isModelLoad = True

    return Response({'Status': "Model loaded"})