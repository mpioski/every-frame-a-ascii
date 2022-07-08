import os
import cv2
import math

from concurrent import futures
from PIL import Image as Img, ImageDraw, ImageFont
from video import Video
from natsort import natsorted


class Image(Video):

    def __init__(self, image_dir: str, ascii_dir: str, video_path: str, frame_dir: str, threads: int, fps: int):
        super(Image, self).__init__(video_path=video_path, frame_dir=frame_dir, fps=fps)
        list(map(lambda x: os.makedirs(x, exist_ok=True), [image_dir, ascii_dir]))
        self.ORIGINAL_IMAGE_DIRECTORY = image_dir
        self.ASCII_IMAGE_DIRECTORY = ascii_dir
        self.ASCII_CHARS = ["@", "#", "$", "%", "W", "?", "*", "+", "i", ";", ":", ",", "."]
        self.MULTIPLIER_CONSTANT = len(self.ASCII_CHARS) - 1
        self.THREADS = threads

    @staticmethod
    def resize_image(image, new_width=100):
        width, height = image.size
        ratio = width / new_width
        resized_image = image.resize((int(width/ratio), int(height/ratio)))
        return resized_image, new_width

    @staticmethod
    def grayscale(image):
        grayscale_image = image.convert("L")
        return grayscale_image

    def pixels_to_ascii(self, image, width):

        pixels = image.getdata()
        ascii_row = "".join(
            [self.ASCII_CHARS[(self.MULTIPLIER_CONSTANT * pixel) // 256] if bool(i % width) else '\n' +
             self.ASCII_CHARS[(self.MULTIPLIER_CONSTANT * pixel) // 256] for i, pixel in enumerate(pixels)])
        return ascii_row[1:]

    def start(self):
        total_images = os.listdir(self.ORIGINAL_IMAGE_DIRECTORY)
        images_per_thread = self.calculate_thread_bath(images=len(total_images))
        threads_images = self.images(total_images=total_images, images_per_thread=images_per_thread)
        self.start_threads(threads_images=threads_images)

    def start_threads(self, threads_images):
        with futures.ThreadPoolExecutor(max_workers=self.THREADS) as executor:
            for thread_images in threads_images:
                executor.submit(self.to_ascii, images=thread_images)

    def calculate_thread_bath(self, images: int) -> int:
        return math.ceil(images / self.THREADS)

    @staticmethod
    def images(total_images, images_per_thread):
        threads_images = []
        for index in range(0, len(total_images), images_per_thread):
            threads_images.append(total_images[index: index + images_per_thread])

        return threads_images

    def to_ascii(self, images):
        for filename in images:
            path = os.path.join(self.ORIGINAL_IMAGE_DIRECTORY, filename)
            image = Img.open(path)
            resized_image, new_width = self.resize_image(image=image)
            resized_gray_image = self.grayscale(resized_image)
            ascii_image = self.pixels_to_ascii(image=resized_gray_image, width=new_width)
            ascii_image_split = ascii_image.split("\n")
            img_height = int(len(ascii_image_split) * 18)
            img_widht = int(len(ascii_image_split[0]) * 10)
            img = Img.new("L", (img_widht, img_height))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("cour.ttf", 16)
            draw.multiline_text((0, 0), str(ascii_image), fill=(255,), font=font,
                                align="center")
            img.save(os.path.join(self.ASCII_IMAGE_DIRECTORY, filename))
            print(filename)

    def to_video(self):
        images = natsorted([img for img in os.listdir(self.ASCII_IMAGE_DIRECTORY)])
        frame = cv2.imread(os.path.join(self.ASCII_IMAGE_DIRECTORY, images[0]))
        height, width, layers = frame.shape
        video_name = 'final.mp4'
        cv2.VideoWriter_fourcc(*'MP4V')
        video = cv2.VideoWriter(video_name, 0x7634706d, self.FPS, (width, height))
        for image in images:
            video.write(cv2.imread(os.path.join(self.ASCII_IMAGE_DIRECTORY, image)))

        video.release()
