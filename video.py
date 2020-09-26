import cv2
import os


class Video:

    def __init__(self, video_path: str, frame_dir: str, fps: int):
        self.VIDEO_PATH = video_path
        self.FRAME_DIRECTORY = frame_dir
        self.FRAME_FILENAME = '%d.jpg'
        self.FPS = fps

    def to_frame(self):
        video = cv2.VideoCapture(self.VIDEO_PATH)
        retval, image = video.read()
        count = 0
        while retval:
            destiny_path = os.path.join(self.FRAME_DIRECTORY, self.FRAME_FILENAME % count)
            cv2.imwrite(destiny_path, image)
            retval, image = video.read()
            count += 1
