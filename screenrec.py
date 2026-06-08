import cv2
import numpy as np
from PIL import ImageGrab
import os
import time

def start_screen_recorder(output_filename="screen_record.mp4", fps=24.0):
    screen_size = ImageGrab.grab().size
    
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    
    out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)
    
    print("\n[!] Screen Recorder Initialized.")
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
