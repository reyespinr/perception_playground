from flask import Flask, render_template, Response, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, UserMixin, login_required, logout_user, current_user
import cv2

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

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
    return User.query.get(int(user_id))

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
    cameras = list(range(5))  # [0, 1, 2, 3, 4]
    return render_template('index.html', cameras=cameras)

@app.route('/video_feed/<int:camera_id>')
@login_required
def video_feed(camera_id):
    # Set the camera source based on the camera_id (if you have multiple cameras)
    global video_capture
    video_capture = cv2.VideoCapture(camera_id)
    
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/command', methods=['POST'])
# def command():
#     # Get the command data from the AJAX post
#     cmd = request.form.get('cmd')
    
#     # Print the command to the Flask server console
#     print(f"Received Command: {cmd}")
    
#     # Normally, you'd publish this to ROS2, but for now, we're just printing it.
    
#     # Return a success message
#     return jsonify({'message': 'Command received!'})

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    direction = data['direction']
    # print(f"Received command: {direction}")
    return jsonify({'status': 'OK'})


def gen_frames():
    """Generate frames for video stream."""
    global video_capture
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create SQLite database if it doesn't exist
    app.run(host='0.0.0.0', debug=True, threaded=True)
