import pyrealsense2 as rs
import numpy as np
import cv2

# Setup the pipeline for D435
d435_pipeline = rs.pipeline()
d435_config = rs.config()

# Configure and start the stream (color & depth) for D435
d435_config.enable_device("018322070175")
d435_config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
d435_config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
d435_pipeline.start(d435_config)

# Setup the pipeline for T265
t265_pipeline = rs.pipeline()
t265_config = rs.config()

# Configure and start the fisheye streams for the T265
t265_config.enable_device("224622112228")
t265_config.enable_stream(rs.stream.fisheye, 1, 848, 800, rs.format.y8, 30)
t265_config.enable_stream(rs.stream.fisheye, 2, 848, 800, rs.format.y8, 30)
t265_pipeline.start(t265_config)

try:
    while True:
        # Get frames for D435
        frames = d435_pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        # Get frames for T265
        frames2 = t265_pipeline.wait_for_frames()
        fisheye1_frame = frames2.get_fisheye_frame(1)
        fisheye2_frame = frames2.get_fisheye_frame(2)

        # Convert images to numpy arrays for D435
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # Convert images to numpy arrays for T265
        fisheye1_image = np.asanyarray(fisheye1_frame.get_data())
        fisheye2_image = np.asanyarray(fisheye2_frame.get_data())

        # Apply colormap on depth image
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        # Display all feeds
        cv2.imshow('Color Feed', color_image)
        cv2.imshow('Depth Feed', depth_colormap)
        cv2.imshow('Fisheye1 Feed', fisheye1_image)
        cv2.imshow('Fisheye2 Feed', fisheye2_image)

        # Break loop if 'esc' key is pressed
        if cv2.waitKey(1) & 0xFF == 27:
            break

finally:
    d435_pipeline.stop()
    t265_pipeline.stop()
    cv2.destroyAllWindows()
