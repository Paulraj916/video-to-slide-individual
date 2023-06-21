import os
import time
import cv2
import imutils
import shutil
import time
from pptx1 import pptx1
import glob

pptx1 = pptx1("video")

class v2s:
    def __init__(self,make):
        self.make = make
        OUTPUT_SLIDES_DIR = f"./output"

        framerate = 3                   # no.of frames per second that needs to be processed, fewer the count faster the speed
        warmup = framerate              # initial number of frames to be skipped
        fgbshistory = framerate * 15    # no.of frames in background object
        varthreshold = 16               # Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.
        detectshadows = False           # If true, the algorithm will detect shadows and mark them.
        minipercent = 0.1               # min % of diff between foreground and background to detect if motion has stopped
        maxpercent = 3                  # max % of diff between foreground and background to detect if frame is still in motion

        def get_frames(video_path):

            vs = cv2.VideoCapture(video_path)
            framerate=vs.get(cv2.CAP_PROP_FPS) 
            if not vs.isOpened():
                raise Exception(f'unable to open file {video_path}')

            total_frames = vs.get(cv2.CAP_PROP_FRAME_COUNT)
            frame_time = 0
            frame_count = 0
            print("total_frames: ", total_frames)
            print("framerate", framerate)

            while True:

                vs.set(cv2.CAP_PROP_POS_MSEC, frame_time * 1000)    # move frame to a timestamp
                frame_time += 1/framerate

                (_, frame) = vs.read()

                if frame is None:
                    break

                frame_count += 1
                yield frame_count, frame_time, frame

            vs.release()

        def detect_unique_screenshots(video_path, output_folder_screenshot_path):

            fgbg = cv2.createBackgroundSubtractorMOG2(history=warmup, varThreshold=varthreshold,detectShadows=detectshadows)

            captured = False
            start_time = time.time()
            (W, H) = (None, None)

            screenshoots_count = 0
            for frame_count, frame_time, frame in get_frames(video_path):
                orig = frame.copy() # clone the original frame (so we can save it later), 
                frame = imutils.resize(frame, width=600) # resize the frame
                mask = fgbg.apply(frame) # apply the background subtractor

                if W is None or H is None:
                    (H, W) = mask.shape[:2]

                p_diff = (cv2.countNonZero(mask) / float(W * H)) * 100

                if p_diff < minipercent and not captured and frame_count > warmup:
                    captured = True
                    filename = f"{screenshoots_count:03}_{round(frame_time/60, 2)}.png"

                    path = os.path.join(output_folder_screenshot_path, filename)
                    print("saving {}".format(path))
                    cv2.imwrite(path, orig)
                    img1 = cv2.imread(path)
                    img2 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                    pptx1.convert_screenshots_to_pptx(img2,path)
                    screenshoots_count += 1

                elif captured and p_diff >= maxpercent:
                    captured = False
            print(f'{screenshoots_count} screenshots Captured!')
            print(f'Time taken {time.time()-start_time}s')
            return 

        def initialize_output_folder(video_path):
            '''Clean the output folder if already exists'''
            output_folder_screenshot_path = f"{OUTPUT_SLIDES_DIR}/{video_path.rsplit('/')[-1].split('.')[0]}"

            if os.path.exists(output_folder_screenshot_path):
                shutil.rmtree(output_folder_screenshot_path)

            os.makedirs(output_folder_screenshot_path, exist_ok=True)
            print('initialized output folder', output_folder_screenshot_path)
            return output_folder_screenshot_path

        for img in glob.glob("video/*.mp4"):
            video_path =img
        output_folder_screenshot_path = initialize_output_folder(video_path)
        detect_unique_screenshots(video_path, output_folder_screenshot_path)