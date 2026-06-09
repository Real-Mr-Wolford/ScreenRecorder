import cv2
import numpy as np
from PIL import ImageGrab
import os
import time

filename = input("Enter the output filename (with extension, for example 'recording.mp4'): ")

#  mouse coordinate tracker
ix, iy = -1, -1
bx, by, bw, bh = 0, 0, 0, 0
drawing = False
selection_complete = False

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, bx, by, bw, bh, drawing, selection_complete
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = param.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            cv2.imshow("Select Recording Area (Drag & Press ENTER)", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bx = min(ix, x)
        by = min(iy, y)
        bw = abs(ix - x)
        bh = abs(iy - y)
        selection_complete = True
        
        img_copy = param.copy()
        cv2.rectangle(img_copy, (bx, by), (bx + bw, by + bh), (0, 255, 0), 2)
        cv2.imshow("Select Recording Area (Drag & Press ENTER)", img_copy)

def get_user_selected_roi():
    global bx, by, bw, bh, selection_complete
    
    
    selection_complete = False
    bx, by, bw, bh = 0, 0, 0, 0

    screenshot = ImageGrab.grab()
    canvas = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    window_name = "Select Recording Area (Drag & Press ENTER)"
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    
    cv2.imshow(window_name, canvas)
    cv2.setMouseCallback(window_name, draw_rectangle, param=canvas)
    
    print("\nDrag a box over your screen to select the region, then press ENTER.")
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key in [13, 32]:  # Enter or Space
            if selection_complete and bw > 10 and bh > 10:
                break
            else:
                print("Please drag a clear box before pressing Enter!")
        elif key == 27:  # Escape key to fall back to full screen 
            cv2.destroyWindow(window_name)
            print("Selection canceled. Defaulting to full screen mode.")
            return None
            
    cv2.destroyWindow(window_name)
    return (bx, by, bw, bh)

def start_screen_recorder(output_filename=filename):
    
    roi = get_user_selected_roi()
    
    if roi:
        left, top, width, height = roi
        right = left + width
        bottom = top + height
        bbox = (left, top, right, bottom)
    else:
        
        bbox = None 

    record_start = time.time()
    frames = []
    timestamps = []  

    print("\nScreen Recorder Started.")
    print("\nPRESS 'q' INSIDE THE VIDEO WINDOW TO STOP RECORDING...\n")

    try:
        while True:
            t = time.time()
            
            img = ImageGrab.grab(bbox=bbox)
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            frames.append(frame)
            timestamps.append(t - record_start)  # seconds since start

            small_frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
            cv2.imshow("Recording Preview", small_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nRecording stopped.")

    finally:
        if not frames:
            print("[!] No frames recorded.")
            cv2.destroyAllWindows()
            return

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
            extension = "mp4v"

        fourcc = cv2.VideoWriter_fourcc(*str(extension)) 
        
        
        # MP4: mp4v, H264, avc1, X264 | AVI: XVID, DIVX, MJPG, I420 | WebM: VP08, VP09

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
