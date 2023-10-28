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
function sendCommand(direction) {
    console.log(`Sending command: ${direction}`);

    // Convert direction to linear_x and angular_z values
    let payload;
    switch(direction) {
        case 'forward':
            payload = { 'linear_x': 1.0, 'angular_z': 0.0, 'direction': 'forward' };
            break;
        case 'backward':
            payload = { 'linear_x': -1.0, 'angular_z': 0.0, 'direction': 'backward' };
            break;
        case 'left':
            payload = { 'linear_x': 0.0, 'angular_z': 1.0, 'direction': 'left' };
            break;
        case 'right':
            payload = { 'linear_x': 0.0, 'angular_z': -1.0, 'direction': 'right' };
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
        handleJoystickMovement(gp.axes[0], gp.axes[1]); // Only process movement for now
        // We can add the turbo and other button functionality in the next phase
    }
}

function handleJoystickMovement(xAxis, yAxis) {
    let command;

    if (xAxis > 0.5) {
        command = 'right';
    } else if (xAxis < -0.5) {
        command = 'left';
    } else if (yAxis > 0.5) {
        command = 'backward';
    } else if (yAxis < -0.5) {
        command = 'forward';
    } else {
        command = 'stop';
    }

    sendCommand(command);
}