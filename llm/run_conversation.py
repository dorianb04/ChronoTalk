from langchain.llms import HuggingFacePipeline

print("downloading model...")
hf = HuggingFacePipeline.from_model_id(
    model_id="Intel/neural-chat-7b-v3-1",
    task="text-generation",
    pipeline_kwargs={"max_new_tokens": 500},
)


from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

print("creating the llm_chain...")
def create_chain(llm):
    template = """<|im_start|>system
    The following is a conversation between a human and Napoleon. Napoleon gives answer in only less than 5 sentences. His task is to converse with people so that they can learn more about you and your history. By interacting with napoleon, the human will be able to change the course of history.<|im_end|>

    {chat_history}
    <|im_start|>user
    {user_input}<|im_end|>
    <|im_start|>assistant"""

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


print("starting the conversation...")
def converse_llm(llm):
    llm_chain = create_chain(llm)
    
    prefix = "You present your history starting from the french revolution to the beginning of waterloo battle without presenting the real outcome of what happened. At some keypoint in the battle, you present the situation, and ask the me of what you should do so that another outcome happens than the lost of the french army."
    response = llm_chain.predict(user_input=prefix)
    print(response)
    for i in range(10):
        response = llm_chain.predict(user_input=input("Your answer to Napoleon: "))
        print(response)

converse_llm(hf)