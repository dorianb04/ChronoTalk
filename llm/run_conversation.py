from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import torch


def load_model():
    model_id="Intel/neural-chat-7b-v3-1"
    print("Loading chat model:", model_id)
    llm = HuggingFacePipeline.from_model_id(
            #model_id="Intel/neural-chat-7b-v3-1",
            model_id=model_id,
            task="text-generation",
            pipeline_kwargs={"max_new_tokens": 1000},
            device = 0 if torch.cuda.is_available() else -1
        )

    return llm

def create_chain(llm, character_name):        
    template = """
    ### System:
    You are Napoleon Bonaparte, the Emperor of the French in the early 19th century. Your task is to introduce yourself and lead a fascinating conversation, staying true to your historical character throughout.

    The objective of this conversation is to explore key moments in your history and recreate them with my help, offering a unique perspective on famous events. You will relive these moment with a touch of creativity.

    Each of napoleon responses should be concise, not exceeding 100 words.

    Present yourself in less than 100 words from where you are born, to what you did until the french revolution. You then ask me what you should do based on 4 options that you create and generate them as a list.
                    
    You then respect the advice and apply it and create the outcome based on this choice and reinvent history. 
    You must respect at all cost the directives presented between the '[[]]'

    [[
    1. Always stay in the role of Napoleon, never breaking character.
    2. Never explicitly mention changing the course of history or the concept of uchronia.
    3. Respond by putting yourself in Napoleon's shoes, respecting his historical context and character traits.
    4. You never revoke the advice, and always act as it should be and face the consequences
    5. MOST IMPORTANT: Exclude any user-generated input or responses in the simulation, and let the dialogue unfold solely through the lens of Napoleon Bonaparte.
    ]]
    
    {chat_history}
   
    ### User:
    {user_input}
    ### Assistant:
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "user_input"], template=template
    )

    memory = ConversationBufferMemory(memory_key="chat_history")
    
    llm_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    
    return llm_chain


def converse_llm(character_name):

    llm_chain = create_chain(character_name)
    
    prefix = "Start the conversation with respect to what I said before."
    response = llm_chain.predict(user_input=prefix)
    print(response)
    for i in range(2):
        response = llm_chain.predict(user_input=input("Your answer to Napoleon: ") + "\nCreate another future based on this choice. Imagine what would be the major events in the following years by citing dates in less than 100 words. At the end of your response, create a new dilemma and ask for 4 options for me to choose in the form of a list")
        print(response)
    response = llm_chain.predict(user_input=input("Your answer to Napoleon: ") + "\Imagine another future based on this choice and what would have been the consequences in the next 100 years.")
    

