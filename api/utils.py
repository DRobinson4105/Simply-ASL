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
Do not respond with anything but the ASL Gloss and always respond with ASL Gloss no matter what they
respond or ask.
"""

prompt_template = PromptTemplate(input_variables=['history', 'input'], template=custom_prompt)

memory = ConversationBufferMemory()

conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template
)

def text2gloss(text):
    return conversation_chain.invoke(input=text)['response'][7:-8]

#TODO
def gloss2video(gloss):
    pass

#TODO
def video2pose(video):
    pass

def intermediatePose(pose):
    if len(pose) == 0: return []

    lst = pose[0]

    for j in range(1, len(pose)):
        lst.extend([lst[j-1][-1] + i * (lst[i][0] - lst[j-1][-1]) / 31 for i in range(1, 31)])
        lst.extend(pose[j])

    return lst

#TODO
def pose2vis(pose):
    pass

def visualize(text):
    gloss = text2gloss(text)
    video = gloss2video(gloss)
    pose = video2pose(video)
    vis = pose2vis(pose)
    return vis
