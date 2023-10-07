import pyrealsense2 as rs
import numpy as np

# Create a pipeline object. This object configures the streaming camera and owns it's handle
pipeline = rs.pipeline()

# Start streaming
profile = pipeline.start()

while True:
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    
    # Convert images to numpy arrays
    color_image = np.asanyarray(color_frame.get_data())
    # ... your processing here ...

pipeline.stop()