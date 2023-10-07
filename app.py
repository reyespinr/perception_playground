# app.py
from flask import Flask
from config import db, login_manager
from routes import routes  # Importing routes

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)
login_manager.init_app(app)

# Registering the blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create SQLite database if it doesn't exist
    app.run(host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
