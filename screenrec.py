import cv2
import numpy as np
from PIL import ImageGrab
import os
import time

def start_screen_recorder(output_filename="screen_record.mp4", fps=24.0):
    screen_size = ImageGrab.grab().size
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") #here you can choose any codec you want. If you want to switch to .avi, replace *"mp4v" with *"avi". Here are some more codecs
    #you can use. Be sure to change the filename extension as well :) 
    # MP4 File Container (.mp4 extension)
    # ----------------------------------
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Standard MPEG-4. Native to OpenCV and universally supported across OS platforms.
    # fourcc = cv2.VideoWriter_fourcc(*"H264")  # Advanced Video Coding. Offers superior compression but requires H.264 binaries on the host system.
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
    
    out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)
    
    print("\n[!] Screen Recording")
    print(f"[!] Resolution: {screen_size[0]}x{screen_size[1]} | Target FPS: {fps}")
    print("[!] PRESS 'q' INSIDE THE VIDEO WINDOW TO STOP RECORDING...\n")
    
    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)

    try:
        while True:
            img = ImageGrab.grab()
            img_np = np.array(img)
        
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            out.write(frame)
            
            small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            cv2.imshow("TerminalOS - Recording Preview", small_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\n[!] Recording interrupted by user.")
        
    finally:
        
        out.release()
        cv2.destroyAllWindows()
        print(f"\n[+] Success! Recording saved as: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    start_screen_recorder()
