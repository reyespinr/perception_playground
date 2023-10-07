from flask import Blueprint, render_template, Response, redirect, url_for, request, flash, jsonify
from config import db, login_manager
from flask_login import login_user, login_required, logout_user
from models import User
from camera import CameraManager
import cv2
import pyrealsense2 as rs
import numpy as np  # Ensure numpy is imported

routes = Blueprint('routes', __name__)

camera_manager = CameraManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('routes.index'))
        flash('Invalid username or password.')

    return render_template('login.html')

@routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

@routes.route('/')
@login_required
def index():
    available_feeds = camera_manager.get_available_feeds()
    print("Available Feeds:", available_feeds)
    return render_template('index.html', feeds=available_feeds)

@routes.route('/video_feed/<string:camera_id>')
@login_required
def video_feed(camera_id):
    try:
        serial_number, stream_type = camera_id.split(':')
        stream_type = stream_type.title()
    except ValueError:
        return "Invalid Camera ID format", 400

    def generate_frames():
        while True:
            frame = camera_manager.get_frame(serial_number, stream_type)
            
            # Ensure the frame is valid and in numpy ndarray format
            if frame is not None and isinstance(frame, np.ndarray):
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            else:
                print(f"routes.py: No frame received for camera with serial number {serial_number}")

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@routes.route('/command', methods=['POST'])
def command():
    print("Command received!")
    data = request.json
    direction = data['direction']
    print(f"Received command: {direction}")
    return jsonify({'status': 'OK'})
