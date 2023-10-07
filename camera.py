import pyrealsense2 as rs
import numpy as np
import threading
import cv2

class Camera:
    FEEDS = {
        'Intel RealSense D435': ['Color', 'Depth', 'Infrared1', 'Infrared2'],
        'Intel RealSense T265': ['Fisheye1', 'Fisheye2']
    }

    def __init__(self, serial_number, device_name):
        self.serial_number = serial_number
        self.device_name = device_name
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.pipeline_started = False
        self.lock = threading.Lock()
        self.possible_feeds = Camera.FEEDS.get(device_name, [])

    def start(self):
        with self.lock:
            if not self.pipeline_started:
                self.setup_config()
                profile = self.pipeline.start(self.config)
                if profile:
                    self.pipeline_started = True
                    print(f"Started pipeline for serial number: {self.serial_number}")
                else:
                    print(f"Failed to start pipeline for serial number: {self.serial_number}")

    def stop(self):
        with self.lock:
            if self.pipeline_started:
                self.pipeline.stop()
                self.pipeline_started = False
                print(f"Stopped pipeline for serial number: {self.serial_number}")

    def get_frame(self, feed_type='Color'):
        if not self.pipeline_started:
            print(f"Pipeline for serial {self.serial_number} is not started. Attempting to start now.")
            self.start()

        try:
            frames = self.pipeline.wait_for_frames()

            if feed_type == 'Color' and self.device_name == 'Intel RealSense D435':
                color_frame = frames.get_color_frame()
                return np.asanyarray(color_frame.get_data())

            elif feed_type == 'Depth' and self.device_name == 'Intel RealSense D435':
                depth_frame = frames.get_depth_frame()
                depth_image = np.asanyarray(depth_frame.get_data())
                return cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            
            elif feed_type == 'Infrared1' and self.device_name == 'Intel RealSense D435':
                ir_frame_lef = frames.get_infrared_frame(1)
                return np.asanyarray(ir_frame_lef.get_data())
            
            elif feed_type == 'Infrared2' and self.device_name == 'Intel RealSense D435':
                ir_frame_right = frames.get_infrared_frame(2)
                return np.asanyarray(ir_frame_right.get_data())

            elif feed_type == 'Fisheye1' and self.device_name == 'Intel RealSense T265':
                fisheye1_frame = frames.get_fisheye_frame(1)
                return np.asanyarray(fisheye1_frame.get_data())

            elif feed_type == 'Fisheye2' and self.device_name == 'Intel RealSense T265':
                fisheye2_frame = frames.get_fisheye_frame(2)
                return np.asanyarray(fisheye2_frame.get_data())

            else:
                print(f"Unsupported feed type {feed_type} for serial number: {self.serial_number}. Available feeds for the device are: {self.possible_feeds}")
                return None

        except Exception as e:
            print(f"Error fetching frame for serial number {self.serial_number}: {e}")
            return None

    def setup_config(self):
        self.config.enable_device(self.serial_number)
        if self.device_name == 'Intel RealSense D435':
            self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
            self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
            self.config.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)
            self.config.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)

        elif self.device_name == 'Intel RealSense T265':
            self.config.enable_stream(rs.stream.fisheye, 1, 848, 800, rs.format.y8, 30)
            self.config.enable_stream(rs.stream.fisheye, 2, 848, 800, rs.format.y8, 30)

class CameraManager:
    def __init__(self):
        self.cameras = {}
        # Dynamically adding cameras
        context = rs.context()
        devices = context.query_devices()

        if len(devices) == 0:
            print("No RealSense devices detected")
        else:
            for device in devices:
                serial_number = device.get_info(rs.camera_info.serial_number)
                name = device.get_info(rs.camera_info.name)
                del device

                print(f'Found device: {name} {serial_number}')
                self.add_camera(serial_number, name)

        # Print detected cameras for debugging
        print("Detected Cameras:", self.cameras)

    def add_camera(self, serial_number, device_name):
        camera = Camera(serial_number, device_name)
        camera.start()  # Ensure the camera pipeline starts
        self.cameras[serial_number] = camera
        print(f"Added camera with serial number: {serial_number}")

    def get_frame(self, serial_number, feed_type='Color'):
        if serial_number in self.cameras:
            return self.cameras[serial_number].get_frame(feed_type)
        print(f"Camera with serial number {serial_number} not found!")
        return None

    def get_available_feeds(self):
        feeds = []
        for serial, camera in self.cameras.items():
            for feed in camera.possible_feeds:
                feeds.append((serial, camera.device_name + " - " + feed))
        return feeds
