from rest_framework.response import Response
from rest_framework.decorators import api_view
import sys
import time

sys.path.append("/home/boucherd/genAI/ChronoTalk")

from llm import run_conversation
from tts import tts_api

# Initialization of the global variables
llm_chain = None
conv_iteration = 0
isModelLoad = False
llm = None
tts_model = None

@api_view(['POST'])
def postMessage(request):
    global conv_iteration
    global llm_chain
    global tts_model

    # Get characterName and message from the request data
    character_name = request.data.get('characterName', '')
    message = request.data.get('message', '')
    print(conv_iteration)
    # Your processing logic here...
    
    conv_user_input_conditioning = """
    \nCreate another future based on this choice in less than 100 words. You are still napoleon, you imagine what would be the major events in the following years by citing dates. At the end of your response, create a new dilemma and ask me for 4 options for me to choose in the form of a list like this:
        <br>1. ...
        <br>2. ...
        <br>3. ...
        <br>4. ...
    """

    end_user_input_conditioning = """
    \nThis is the end of our conversation. You then imagine what would be the major events in the following years and wrap up all of what we said in less than 100 words. Finish the conversation as an emperor."""
    
    if conv_iteration < 5:
        response = llm_chain.predict(user_input= message + conv_user_input_conditioning)
        conv_iteration += 1
    else:
        response = llm_chain.predict(user_input= message + end_user_input_conditioning)
    
    print(response)

    print(response.split('<br>')[0])

    tts_api.main(tts_model, character_id="2",text_prompt=response.split('<br>')[0], prompt_id=character_name)

    response = response[:4].replace("\n", "") + response[4:].replace("\n", "<br>")

    # Return a response
    response_data = {
        'MP4_path': "/somepath/file.mp4",
        'CHAR_response': response,
        # Add any other data you want to include in the response
    }
    return Response(response_data)

@api_view(['GET'])
def getFirstMessage(request):
    global conv_iteration
    global llm_chain
    global llm
    global tts_model

    llm_chain = run_conversation.create_chain(llm, '')

    character_name = request.query_params.get('characterName', '')

    prefix = """Start the conversation with respect to what I said before. You tell me about your history until the end of the french revolution. Then Create a new dilemma and generate 4 options for me to choose in the form of a list like this:
        <br>1. ...
        <br>2. ...
        <br>3. ...
        <br>4. ...
    """
    
    message = llm_chain.predict(user_input=prefix)
    #message ="e"

    tts_api.main(tts_model, character_id="2",text_prompt=message.split('<br>')[0], prompt_id=character_name)
   
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
    global llm
    global tts_model
    
    if isModelLoad:
        return Response({'Status': "Model already loaded"})
    
    else:
        # Instanciation of the model chain
        llm = run_conversation.load_model()

        # Instanciation of TTS model
        tts_model = tts_api.model_loader()

        isModelLoad = True

    return Response({'Status': "Model loaded"})