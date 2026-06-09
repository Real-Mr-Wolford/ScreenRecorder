Records a silent video of your screen, now with area drag! 

Video formats:

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
