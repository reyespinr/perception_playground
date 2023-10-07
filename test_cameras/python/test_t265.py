# import pyrealsense2 as rs
# import cv2
# import numpy as np

# # Set up a mutex to share data between threads 
# from threading import Lock
# frame_mutex = Lock()
# frame_data = {"left"  : None,
#               "right" : None,
#               "timestamp_ms" : None
#               }

# def callback(frame):
#     global frame_data
#     if frame.is_frameset():
#         frameset = frame.as_frameset()
#         f1 = frameset.get_fisheye_frame(1).as_video_frame()
#         f2 = frameset.get_fisheye_frame(2).as_video_frame()
#         left_data = np.asanyarray(f1.get_data())
#         right_data = np.asanyarray(f2.get_data())
#         ts = frameset.get_timestamp()
#         frame_mutex.acquire()
#         frame_data["left"] = left_data
#         frame_data["right"] = right_data
#         frame_data["timestamp_ms"] = ts
#         frame_mutex.release()

# # Declare RealSense pipeline, encapsulating the actual device and sensors
# pipe = rs.pipeline()
# cfg = rs.config()

# # Configure and start the fisheye streams for the T265
# cfg.enable_device("224622112228")
# cfg.enable_stream(rs.stream.fisheye, 1, 848, 800, rs.format.y8, 30)
# cfg.enable_stream(rs.stream.fisheye, 2, 848, 800, rs.format.y8, 30)

# # Start the pipeline
# pipe.start(cfg, callback)

# try:
#     profiles = pipe.get_active_profile()
#     streams = {"left"  : profiles.get_stream(rs.stream.fisheye, 1).as_video_stream_profile(),
#                 "right" : profiles.get_stream(rs.stream.fisheye, 2).as_video_stream_profile()}
#     while True:
        
#         # Check if the camera has acquired any frames
#         frame_mutex.acquire()
#         valid = frame_data["timestamp_ms"] is not None
#         frame_mutex.release()

#         # If frames are ready to process
#         if valid:
#             # Hold the mutex only long enough to copy the stereo frames
#             frame_mutex.acquire()
#             frame_copy = {"left"  : frame_data["left"].copy(),
#                           "right" : frame_data["right"].copy()}
#             frame_mutex.release()
                     
      
#             left_image = np.asanyarray(frame_copy["left"])
#             right_image = np.asanyarray(frame_copy["right"])

#             # Display the images side by side
#             cv2.imshow('T265 Left Fisheye', left_image)
#             cv2.imshow('T265 Right Fisheye', right_image)

#         # Exit if 'esc' key is pressed
#         if cv2.waitKey(1) & 0xFF == 27:
#             break

# finally:
#     pipe.stop()
#     cv2.destroyAllWindows()

import pyrealsense2 as rs
import numpy as np
import cv2

# Setup the pipeline
pipeline = rs.pipeline()
config = rs.config()

# Configure and start the fisheye streams for the T265
config.enable_device("224622112228")
config.enable_stream(rs.stream.fisheye, 1, 848, 800, rs.format.y8, 30)
config.enable_stream(rs.stream.fisheye, 2, 848, 800, rs.format.y8, 30)
pipeline.start(config)

try:
    while True:
        # Get frames
        frames = pipeline.wait_for_frames()
        fisheye1_frame = frames.get_fisheye_frame(1)
        fisheye2_frame = frames.get_fisheye_frame(2)

        # Convert images to numpy arrays
        fisheye1_image = np.asanyarray(fisheye1_frame.get_data())
        fisheye2_image = np.asanyarray(fisheye2_frame.get_data())

        # Display both images
        cv2.imshow('Fisheye1 Feed', fisheye1_image)
        cv2.imshow('Fisheye2 Feed', fisheye2_image)

        # Break loop if 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()

