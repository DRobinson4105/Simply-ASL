import os
import shutil
import cv2

def get_vid_len(path):
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)  
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)      
    duration = total_frames / fps
    print(duration)
    return duration

def trim(path, out_path):
    video = cv2.VideoCapture(path)
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
   
    output_video = cv2.VideoWriter(out_path, fourcc, fps, (frame_width, frame_height))
    max_frames = int(fps * 1) 
    frame_count = 0
   
    while video.isOpened() and frame_count < max_frames:
        ret, frame = video.read()
        if not ret:
            break
        output_video.write(frame)
        frame_count += 1
    
    video.release()
    output_video.release()
    print(f"Trimmed video saved to {out_path}")

def copy_trim(dir, out_dir):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)
        output_path = os.path.join(out_dir, file_name)

        if file_name.lower().endswith('.mov'):
            print(f"Processing: {file_name}")
            video_duration = get_vid_len(file_path)
        
            if video_duration:
                if video_duration > 1:
                    trim(file_path, output_path)
                else:
                    shutil.copy(file_path, output_path)
                    print(f"Copied: {file_name} (Duration: {video_duration:.2f})")
            else:
                print(f"Failed to process {file_name}")

copy_trim('alphabet', 'alphabet60')