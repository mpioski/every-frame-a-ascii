import argparse
from image import Image


class Main:

    def __init__(self, video_path: str, threads: int, fps: int):
        frame_dir = 'frames/'
        ascii_dir = 'ascii_frames/'
        self.convert = Image(image_dir=frame_dir, ascii_dir=ascii_dir, video_path=video_path, frame_dir=frame_dir,
                             threads=int(threads), fps=int(fps))

    def run(self):
        print("Spliting video into frames...")
        self.convert.to_frame()
        print("Success!")
        print("Converting every frame to ascii...")
        self.convert.start()
        print("Success!")
        print("Converting every ascii frame to video...")
        self.convert.to_video()
        print("Success!")


if __name__ == "__main__":
    args = argparse.ArgumentParser(description='Convert videos to ASCII')
    args.add_argument('-vp', '--video-path', action='store', help='Video Path and filename', required=True)
    args.add_argument('-t', '--threads', nargs='?', help='Number of threads', default=1)
    args.add_argument('-fps', '--fps', nargs='?', help='Number of FPS in converted video', default=25)

    main = Main(video_path=args.parse_args().video_path, threads=args.parse_args().threads, fps=args.parse_args().fps)
    main.run()
