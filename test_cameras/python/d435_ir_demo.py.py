import pyrealsense2 as rs
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()

# Configure the IR streams of the D435
config.enable_stream(rs.stream.infrared, 1, 1280, 720,
                     rs.format.y8, 30)  # left IR camera
config.enable_stream(rs.stream.infrared, 2, 1280, 720,
                     rs.format.y8, 30)  # right IR camera

# Start the pipeline
pipeline.start(config)

try:
    while True:
        # Get the next set of frames from the camera
        frames = pipeline.wait_for_frames()

        # Get both IR frames
        ir_frame_left = frames.get_infrared_frame(1)
        ir_frame_right = frames.get_infrared_frame(2)

        # Convert the IR frames to numpy arrays for visualization
        ir_image_left = np.asanyarray(ir_frame_left.get_data())
        ir_image_right = np.asanyarray(ir_frame_right.get_data())

        # Display the images
        cv2.imshow('IR Left', ir_image_left)
        cv2.imshow('IR Right', ir_image_right)

        # Break the loop when 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
