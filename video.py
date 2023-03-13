import os
import io
import uuid
import sys
import yaml
import traceback

with open('./config.yaml', 'r') as fd:
    opts = yaml.safe_load(fd)

sys.path.insert(0, './white_box_cartoonizer/')

import cv2
import flask
from PIL import Image
import numpy as np
import skvideo.io


from cartoonize import WB_Cartoonize

config={}
config['UPLOAD_FOLDER_VIDEOS'] = 'static/uploaded_videos'
config['CARTOONIZED_FOLDER'] = 'static/cartoonized_images'

config['OPTS'] = opts

## Init Cartoonizer and load its weights 
wb_cartoonizer = WB_Cartoonize(os.path.abspath("white_box_cartoonizer/saved_models/"), opts['gpu'])

def convert_bytes_to_image(img_bytes):
    """Convert bytes to numpy array

    Args:
        img_bytes (bytes): Image bytes read from flask.

    Returns:
        [numpy array]: Image numpy array
    """
    
    pil_image = Image.open(io.BytesIO(img_bytes))
    if pil_image.mode=="RGBA":
        image = Image.new("RGB", pil_image.size, (255,255,255))
        image.paste(pil_image, mask=pil_image.split()[3])
    else:
        image = pil_image.convert('RGB')
    
    image = np.array(image)
    
    return image

def cartooniz_image(fname):
    img = cv2.imread('white_box_cartoonizer/test.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cartoon_image = wbc.infer(img)
    cartoonized_img_name = os.path.join(fname)
    cv2.imwrite(cartoonized_img_name, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
    return True

def cartooniz_video(filename):
    original_video_path = os.path.join(config['UPLOAD_FOLDER_VIDEOS'], filename)
    modified_video_path = os.path.join(config['UPLOAD_FOLDER_VIDEOS'], filename.split(".")[0] + "_modified.mp4")
    
    ## Fetch Metadata and set frame rate
    file_metadata = skvideo.io.ffprobe(original_video_path)
    original_frame_rate = None
    if 'video' in file_metadata:
        if '@r_frame_rate' in file_metadata['video']:
            original_frame_rate = file_metadata['video']['@r_frame_rate']

    if opts['original_frame_rate']:
        output_frame_rate = original_frame_rate
    else:
        output_frame_rate = opts['output_frame_rate']   

    output_frame_rate_number = int(output_frame_rate.split('/')[0])

    #change the size if you want higher resolution :
    ############################
    # Recommnded width_resize  #
    ############################
    #width_resize = 1920 for 1080p: 1920x1080.
    #width_resize = 1280 for 720p: 1280x720.
    #width_resize = 854 for 480p: 854x480.
    #width_resize = 640 for 360p: 640x360.
    #width_resize = 426 for 240p: 426x240.
    width_resize=opts['resize-dim']

    # Slice, Resize and Convert Video as per settings
    if opts['trim-video']:
        #change the variable value to change the time_limit of video (In Seconds)
        time_limit = opts['trim-video-length']
        if opts['original_resolution']:
            os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(os.path.abspath(original_video_path), time_limit, output_frame_rate_number, os.path.abspath(modified_video_path)))
        else:
            os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -t {} -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(os.path.abspath(original_video_path), time_limit, width_resize, output_frame_rate_number, os.path.abspath(modified_video_path)))
    else:
        if opts['original_resolution']:
           os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale=-1:-2 -r {} -c:a copy '{}'".format(os.path.abspath(original_video_path), output_frame_rate_number, os.path.abspath(modified_video_path)))
        else:
            os.system("ffmpeg -hide_banner -loglevel warning -ss 0 -i '{}' -filter:v scale={}:-2 -r {} -c:a copy '{}'".format(os.path.abspath(original_video_path), width_resize, output_frame_rate_number, os.path.abspath(modified_video_path)))
    
    audio_file_path = os.path.join(config['UPLOAD_FOLDER_VIDEOS'], filename.split(".")[0] + "_audio_modified.mp4")
    os.system("ffmpeg -hide_banner -loglevel warning -i '{}' -map 0:1 -vn -acodec copy -strict -2  '{}'".format(os.path.abspath(modified_video_path), os.path.abspath(audio_file_path)))

    cartoon_video_path = wb_cartoonizer.process_video(modified_video_path, output_frame_rate)
    
    ## Add audio to the cartoonized video
    final_cartoon_video_path = os.path.join(config['UPLOAD_FOLDER_VIDEOS'], filename.split(".")[0] + "_cartoon_audio.mp4")
    os.system("ffmpeg -hide_banner -loglevel warning -i '{}' -i '{}' -codec copy -shortest '{}'".format(os.path.abspath(cartoon_video_path), os.path.abspath(audio_file_path), os.path.abspath(final_cartoon_video_path)))

    # Delete the videos from local disk
    os.system("rm {} {} {} {}".format(original_video_path, modified_video_path, audio_file_path, cartoon_video_path))
    
    return True



if __name__ == "__main__":
    # Commemnt the below line to run the Appication on Google Colab using ngrok
    cartooniz_video('aaa.mp4')
