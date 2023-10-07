import pyrealsense2 as rs
import numpy as np
import cv2

# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()

# Configure and start the stream (color & depth)
# Configure the IR streams of the D435
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
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
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()
        ir_frame_left = frames.get_infrared_frame(1)
        ir_frame_right = frames.get_infrared_frame(2)

        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Convert the IR frames to numpy arrays for visualization
        ir_image_left = np.asanyarray(ir_frame_left.get_data())
        ir_image_right = np.asanyarray(ir_frame_right.get_data())

        # Apply colormap on depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Display all images
        cv2.imshow('Color Feed', color_image)
        cv2.imshow('Depth Feed', depth_colormap)
        cv2.imshow('IR Left', ir_image_left)
        cv2.imshow('IR Right', ir_image_right)

        # Break the loop when 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
