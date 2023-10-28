
// Global state
let isTurboMode = false;

// ===========================
// Key Press Logic
// ===========================
document.addEventListener('DOMContentLoaded', (event) => {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
});

function handleKeyDown(event) {
    const keyMappings = {
        'ArrowLeft': 'left',
        'ArrowUp': 'forward',
        'ArrowRight': 'right',
        'ArrowDown': 'backward',
        'w': 'forward',
        'a': 'left',
        's': 'backward',
        'd': 'right'
    };

    if (keyMappings[event.key]) {
        sendCommand(keyMappings[event.key]);
    }
}

function handleKeyUp(event) {
    const keys = ['ArrowLeft', 'ArrowUp', 'ArrowRight', 'ArrowDown', 'w', 'a', 's', 'd'];

    if (keys.includes(event.key)) {
        sendCommand('stop');
    }
}

document.addEventListener('keydown', (event) => {
    switch (event.key) {
        case 'w':
        case 'W':
            document.getElementById('keyW').classList.add('active');
            break;
        case 'a':
        case 'A':
            document.getElementById('keyA').classList.add('active');
            break;
        case 's':
        case 'S':
            document.getElementById('keyS').classList.add('active');
            break;
        case 'd':
        case 'D':
            document.getElementById('keyD').classList.add('active');
            break;
    }
});

document.addEventListener('keyup', (event) => {
    switch (event.key) {
        case 'w':
        case 'W':
            document.getElementById('keyW').classList.remove('active');
            break;
        case 'a':
        case 'A':
            document.getElementById('keyA').classList.remove('active');
            break;
        case 's':
        case 'S':
            document.getElementById('keyS').classList.remove('active');
            break;
        case 'd':
        case 'D':
            document.getElementById('keyD').classList.remove('active');
            break;
    }
});

document.addEventListener('keydown', function(event) {
    switch(event.key) {
        case "ArrowUp":
            document.getElementById('keyW').classList.add('active');
            break;
        case "ArrowDown":
            document.getElementById('keyS').classList.add('active');
            break;
        case "ArrowLeft":
            document.getElementById('keyA').classList.add('active');
            break;
        case "ArrowRight":
            document.getElementById('keyD').classList.add('active');
            break;
    }
});

document.addEventListener('keyup', function(event) {
    switch(event.key) {
        case "ArrowUp":
            document.getElementById('keyW').classList.remove('active');
            break;
        case "ArrowDown":
            document.getElementById('keyS').classList.remove('active');
            break;
        case "ArrowLeft":
            document.getElementById('keyA').classList.remove('active');
            break;
        case "ArrowRight":
            document.getElementById('keyD').classList.remove('active');
            break;
    }
});
// ===========================
// Send Command Logic
// ===========================
// Send Command Logic
function sendCommand(direction) {
    console.log(`Sending command: ${direction}`);

    // Define the scales based on the configuration
    let scaleLinear = isTurboMode ? 1.0 : 0.2;
    let scaleAngular = isTurboMode ? 1.0 : 0.5;

    let payload;
    switch(direction) {
        case 'forward':
            payload = { 'linear_x': scaleLinear, 'angular_z': 0.0, 'direction': 'forward' };
            break;
        case 'backward':
            payload = { 'linear_x': -scaleLinear, 'angular_z': 0.0, 'direction': 'backward' };
            break;
        case 'left':
            payload = { 'linear_x': 0.0, 'angular_z': scaleAngular, 'direction': 'left' };
            break;
        case 'right':
            payload = { 'linear_x': 0.0, 'angular_z': -scaleAngular, 'direction': 'right' };
            break;
        case 'stop':
        default:
            payload = { 'linear_x': 0.0, 'angular_z': 0.0, 'direction': 'stop' };
            break;
    }       
    fetch("/command", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error sending command:', error));
}

// ===========================
// Gamepad Logic
// ===========================
let gamepadInterval;

window.addEventListener("gamepadconnected", function() {
    console.log("Gamepad connected!");
    gamepadInterval = setInterval(checkGamepad, 100); // Check every 100ms
});

window.addEventListener("gamepaddisconnected", function() {
    console.log("Gamepad disconnected!");
    clearInterval(gamepadInterval);
});

function checkGamepad() {
    const gamepads = navigator.getGamepads();

    if (gamepads[0]) {
        const gp = gamepads[0];

        // Handle turbo mode
        if (gp.buttons[4].pressed) {
            isTurboMode = true;
        } else if (gp.buttons[5].pressed) {
            isTurboMode = false;
        }

        handleJoystickMovement(gp.axes[1], gp.axes[2]); // Adjusted for left joystick (y-axis) for forward/backward and right joystick (x-axis) for left/right
        let leftJoyElement = document.getElementById('moveStick');
        if (leftJoyElement) {
            leftJoyElement.style.transform = `translate(-50%, -50%) translate(${gp.axes[0] * 40}px, ${gp.axes[1] * 40}px)`;
        } else {
            console.error(`${'moveStick'} element not found.`);
        }
        let rightJoyElement = document.getElementById('cameraStick');
        if (rightJoyElement) {
            rightJoyElement.style.transform = `translate(-50%, -50%) translate(${gp.axes[2] * 40}px, ${gp.axes[3] * 40}px)`;
        } else {
            console.error(`${'cameraStick'} element not found.`);
        }
        handleGamepadButtons(gp.buttons);
    }
}

function handleJoystickMovement(leftYAxis, rightXAxis) {
    let command;

    if (rightXAxis > 0.5) {
        command = 'right';
    } else if (rightXAxis < -0.5) {
        command = 'left';
    } else if (leftYAxis > 0.5) {
        command = 'backward';
    } else if (leftYAxis < -0.5) {
        command = 'forward';
    } else {
        command = 'stop';
    }

    sendCommand(command);
}

function handleGamepadButtons(buttons) {
    const buttonMappings = [
        { id: 'buttonA', command: 'buttonA', btnIndex: 0 },
        { id: 'buttonB', command: 'buttonB', btnIndex: 1 },
        { id: 'buttonX', command: 'buttonX', btnIndex: 2 },
        { id: 'buttonY', command: 'buttonY', btnIndex: 3 }
    ];

    buttonMappings.forEach(mapping => {
        let buttonElement = document.getElementById(mapping.id);
        if (buttons[mapping.btnIndex].pressed) {
            buttonElement.classList.add('active');
        } else {
            buttonElement.classList.remove('active');
        }
    });
}