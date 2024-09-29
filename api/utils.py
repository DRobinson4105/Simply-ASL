from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os
from pathlib import Path
import numpy as np
from openCVImageGen import getVideo
import cv2

# Initialize the conversation chain globally
load_dotenv()

llm = ChatOpenAI(model_name="gpt-4o-mini")

custom_prompt = """
Human: Here are some examples of translations from English text to ASL gloss:
Examples:
Apples ==> APPLE
Love ==> LIKE
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
I missed it last week ==> LAST WEEK I MISS

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
    text = text.replace('?', '').replace('-', '')
    return conversation_chain.invoke(input=text)['response'][7:-8]

def __load_frames__(token):
    curr = []
    path = Path(f"../pose_dataset/{token}.npy")
    i = 0

    while path.is_file():
        curr.append(np.load(path))
        path = Path(f"../pose_dataset/{token}.npy")
        i += 1

def gloss2pose(gloss):
    pose = []
    tokens = gloss.split()

    for token in tokens:
        if Path(f"../pose_dataset/{token}.npy").is_file():
            pose.append(np.load(f"../pose_dataset/{token}.npy"))
        else:
            for c in token:
                if Path(f"../pose_dataset/{c}.npy").is_file():
                    pose.append(np.load(f"../pose_dataset/{c}.npy"))

    return pose

def intermediatePose(pose):
    if len(pose) == 0: return []

    num_frames = 30
    result = [pose[0]]
    
    for i in range(1, len(pose)):
        start_frame = pose[i-1][-1]
        end_frame = pose[i][0]

        interpolated_frames = np.zeros((num_frames, 133, 3))

        for j in range(num_frames):
            diff = j / (num_frames - 1)
            interpolated_frames[j] = (1 - diff) * start_frame + diff * end_frame

        result.append(interpolated_frames)
        result.append(pose[i])
    
    result = np.concatenate(result, axis=0)
    return result

def pose2video(nparray):
    return getVideo(nparray)

if __name__ == "__main__":
    text = "I missed it last week"
    gloss = text2gloss(text)
    print(gloss)
    pose1 = gloss2pose(gloss)

    print(len(pose1), pose1[0].shape)
    pose2 = np.array(intermediatePose(pose1))
    
    print(pose2.shape)
    video = pose2video(pose2)