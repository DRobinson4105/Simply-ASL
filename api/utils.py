from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Initialize the conversation chain globally
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini")

custom_prompt = """
Human: Here are some examples of translations from English text to ASL gloss:
Examples:
Apples ==> APPLE
you  ==> IX-2P
your  ==> IX-2P
Love ==> LIKE
My ==> IX-1P
Thanks ==> THANK-YOU
am ==> 
and ==> 
be ==>
of ==>
video ==> MOVIE
image ==> PICTURE
conversations ==> TALK
type of ==> TYPE
? ==> QUESTION
Watch ==> SEE
My name is David ==> MY NAME D-A-V-I-D

{history}
Human: {input}
AI: Translate the following English text to ASL Gloss and surround it with tags <gloss> and </gloss>.
"""

prompt_template = PromptTemplate(input_variables=['history', 'input'], template=custom_prompt)

memory = ConversationBufferMemory()

conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template
)

def text2gloss(text):
    return conversation_chain.invoke(input=text)['response']

#TODO
def gloss2video(gloss):
    pass

#TODO
def video2pose(video):
    pass

#TODO
def pose2vis(pose):
    pass

def visualize(text):
    gloss = text2gloss(text)
    video = gloss2video(gloss)
    pose = video2pose(video)
    vis = pose2vis(pose)
    return vis
