import os
import cv2
import re

def safe_path_join(*args):
    return '/'.join(arg.strip('/') for arg in args)

def parse_gloss(gloss):
    return re.split(r'[-\s]+', gloss)

def find_vids(word, gloss_path, alphabet_path):
    if os.path.exists(safe_path_join(gloss_path, f"{word}.mov")):
        return [safe_path_join(gloss_path, f"{word}.mov")]
    videos = []
    word_left = word
    
    while len(word_left) != 0:
        found = False
        if os.path.exists(safe_path_join(gloss_path, f"{word_left}.mov")):
            videos.append(safe_path_join(gloss_path, f"{word_left}.mov"))
            found = True
            break
        
        if not found:
            tmp = word_left[-1].lower()
            if os.path.exists(safe_path_join(alphabet_path, f"{tmp}.mov")):
                videos.append(safe_path_join(alphabet_path, f"{tmp}.mov"))
            word_left = word_left[:-1] 
    
    return videos

def process_gloss(gloss_script, gloss_path, alphabet_path):
    words = parse_gloss(gloss_script)
    result = []
    
    for word in words:
        videos = find_vids(word, gloss_path, alphabet_path)
        result.extend(videos)
    
    return result
 
script = "HELLO-WORLD HOW ARE-YOU"
gloss = "/gloss"
alphabet= "/alphabet60"

breakdown = process_gloss(script, gloss, alphabet)
print("Matched videos:\n")
for video_name in breakdown:
    print(video_name)