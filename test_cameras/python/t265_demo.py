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
