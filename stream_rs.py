from flask import Flask, render_template, Response, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import cv2
import pyrealsense2 as rs
import numpy as np
import threading

pipeline_lock = threading.Lock()

app = Flask(__name__)

pipeline_started = False

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


def setup_d435_config(serial_number):
    """
    Set up configuration for D435 camera with given serial number.
    """
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    return config

# Set up Realsense pipeline
pipeline = rs.pipeline()

serial_number_d435 = "018322070175"
config_d435 = setup_d435_config(serial_number_d435)
pipeline.start(config_d435)
pipeline_started = True


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(80), default='viewer')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    context = rs.context()
    devices = context.query_devices()
    device_names = [dev.get_info(rs.camera_info.name) for dev in devices]

    return render_template('index.html', cameras=device_names)


@app.route('/video_feed/<int:camera_id>')
@login_required
def video_feed(camera_id):
    return Response(gen_frames(camera_id), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/command', methods=['POST'])
def command():
    print("Command received!")
    data = request.json
    direction = data['direction']
    print(f"Received command: {direction}")
    return jsonify({'status': 'OK'})

def start_realsense():
    global pipeline
    # Start streaming
    profile = pipeline.start()
    return pipeline

def gen_frames(camera_id):
    global pipeline_started
    
    # Check if the pipeline is active
    if pipeline_started:
        while True:
            print("Fetching frames...")
            try:
                frames = pipeline.wait_for_frames(2000)  # Timeout after 2000 ms
                color_frame = frames.get_color_frame()

                if not color_frame:
                    print("No color frame received.")
                    continue

                frame = np.asanyarray(color_frame.get_data())
                ret, buffer = cv2.imencode('.jpg', frame)

                if not ret:
                    print("Error encoding frame.")
                    continue

                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                print("Error in frame generation:", e)
    else:
        print("Pipeline not active. Restarting...")
        try:
            with pipeline_lock:
                serial_number_d435 = "018322070175"
                config_d435 = setup_d435_config(serial_number_d435)
                pipeline.start(config_d435)
                pipeline_started = True
                print("Pipeline restarted.")
        except Exception as e:
            print("Error restarting pipeline:", e)

@app.teardown_appcontext
def shutdown_session(exception=None):
    global pipeline_started
    with pipeline_lock:
        if pipeline_started:
            print("Stopping the pipeline...")
            pipeline.stop()
            pipeline_started = False

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create SQLite database if it doesn't exist
    app.run(host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
