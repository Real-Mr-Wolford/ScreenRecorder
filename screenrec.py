import cv2
import numpy as np
from PIL import ImageGrab
import os
import time

filename = input("Enter the output filename (with extension, for example 'recording.mp4'): ")

def start_screen_recorder(output_filename=filename):
    record_start = time.time()
    frames = []
    timestamps = []  

    print("\nScreen Recorder Started.")
    print("\nPRESS 'q' INSIDE THE VIDEO WINDOW TO STOP RECORDING...\n")

    try:
        while True:
            t = time.time()
            img = ImageGrab.grab()
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            frames.append(frame)
            timestamps.append(t - record_start)  # seconds since start

            small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            cv2.imshow("TerminalOS - Recording Preview", small_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    finally:
        total_time = timestamps[-1] if timestamps else 1
        actual_fps = len(frames) / total_time
        print(f"\nCaptured {len(frames)} frames in {total_time:.1f}s at {actual_fps:.1f} fps")

        screen_size = (frames[0].shape[1], frames[0].shape[0])
        extension = filename.split(".")[-1]
        if extension == "avi":
            extension = "XVID"
        elif extension == "mp4":
            extension = "mp4v"
        elif extension == "webm":
            extension = "VP08"
        elif extension == "mov":
            extension = "mp4v"
        elif extension == "mkv":
            extension = "X264"
        else:
            if "." in output_filename:
                output_filename = output_filename.rsplit(".", 1)[0] + ".mp4"
            else:
                output_filename += ".mp4"
        #you can set the default extionsion by using the provided codecs below. Just make sure to change the filename extension as well :)
        fourcc = cv2.VideoWriter_fourcc(*str(extension)) #here you can choose any codec you want. If you want to switch to .avi, replace *"mp4v" with *"avi". Here are some more codecs
        #you can use. Be sure to change the filename extension as well :) 
        # MP4 File Container (.mp4 extension)
        # ----------------------------------
        # fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Standard MPEG-4. Native to OpenCV and universally supported across OS platforms.
        # fourcc = cv2.VideoWriter_fourcc(*"H264")  # Advanced Video Coding. Offers superior compression but requires H.264 linaries on the host system.
        # fourcc = cv2.VideoWriter_fourcc(*"avc1")  # A variant of H.264 frequently used for strict Apple/macOS ecosystem compatibility.
        # fourcc = cv2.VideoWriter_fourcc(*"X264")  # Open-source alternative H.264 encoder.

        # AVI File Container (.avi extension)
        # ----------------------------------
        # fourcc = cv2.VideoWriter_fourcc(*"XVID")  # MPEG-4 variant optimized for AVI. Highly stable fallback for Windows and Linux.
        # fourcc = cv2.VideoWriter_fourcc(*"DIVX")  # Legacy digital video codec. Closely related to XVID.
        # fourcc = cv2.VideoWriter_fourcc(*"MJPG")  # Motion JPEG. Compresses each frame as an independent JPEG. High disk usage, low CPU overhead.
        # fourcc = cv2.VideoWriter_fourcc(*"I420")  # Uncompressed YUV raw video. Produces massive files with zero loss in visual quality.

        # WebM File Container (.webm extension)
        # ------------------------------------
        # fourcc = cv2.VideoWriter_fourcc(*"VP08")  # VP8 codec. Open-source standard designed specifically for web browser playback.
        # fourcc = cv2.VideoWriter_fourcc(*"VP09")  # VP9 codec. Higher efficiency successor to VP8, commonly used for high-definition web video.

        # QuickTime File Container (.mov extension)
        # -----------------------------------------
        # fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # The standard MPEG-4 codec maps cleanly inside Apple's QuickTime wrapper.

        out = cv2.VideoWriter(output_filename, cv2.CAP_FFMPEG, fourcc, actual_fps, screen_size)
        print("Saving video...")
        for i, f in enumerate(frames):
            if i < len(frames) - 1:
                gap = timestamps[i + 1] - timestamps[i]
            else:
                gap = 1 / actual_fps
            dupes = max(1, round(gap * actual_fps))
            for _ in range(dupes):
                out.write(f)

        out.release()
        cv2.destroyAllWindows()
        print(f"\nRecording saved as: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    start_screen_recorder()
