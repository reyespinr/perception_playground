import threading
from pydantic import BaseModel
from dependencies import get_db
from database import engine
from security import get_password_hash, verify_password, create_access_token, get_current_user, NotAuthenticatedException
from models import User, UserRole, Base
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from contextlib import asynccontextmanager
import web_cmd_pub  # assuming you have this imported for ROS2 stuff
import rclpy

# Define the global web_cmd_vel_publisher
web_cmd_vel_publisher = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global web_cmd_vel_publisher

    # Function to run ROS2 spin in a separate thread
    def run_ros_spin():
        rclpy.spin(web_cmd_vel_publisher)

    # Initialize ROS2
    rclpy.init()
    web_cmd_vel_publisher = web_cmd_pub.WebCmdVelPublisher()

    # Start ROS2 spinning in a separate thread
    ros_thread = threading.Thread(target=run_ros_spin)
    ros_thread.start()

    yield

    # Cleanup and shutdown ROS2
    web_cmd_vel_publisher.destroy_node()
    rclpy.shutdown()
    ros_thread.join()  # Ensure ROS2 thread has terminated


class Command(BaseModel):
    linear_x: float
    angular_z: float
    direction: str


# Pass the lifespan context manager to the FastAPI app instantiation
app = FastAPI(lifespan=lifespan)

# Templates and Static setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    try:
        current_user = get_current_user(request, db)
        print(f"Welcome user {current_user}!")
        feeds = [("serial1", "Camera 1 - Color"),
                 ("serial2", "Camera 2 - Depth")]
        return templates.TemplateResponse("index.html", {"request": request, "feeds": feeds})
    except NotAuthenticatedException:
        return RedirectResponse(url="/login")


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": {"error": "Invalid username or password"}})

    token = create_access_token(data={"sub": user.username, "role": user.role})

    response = RedirectResponse(url="/", status_code=303)
    # response.set_cookie(key="access_token", value=f"Bearer {token}")
    response.set_cookie(
        key="access_token", value=f"Bearer {token.decode('utf-8')}" if isinstance(token, bytes) else f"Bearer {token}")

    return response


@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), role: UserRole = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403, detail="Only admin can register new users!")
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(password)
    new_user = User(username=username,
                    hashed_password=hashed_password, role=role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "role": new_user.role}


@app.post("/command")
async def handle_command(data: Command):
    global web_cmd_vel_publisher
    web_cmd_vel_publisher.set_command(data.direction)
    print(data)
    return {"status": "success", "message": f"Command {data} processed"}

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
