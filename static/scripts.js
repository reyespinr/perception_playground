// ===========================
// Loading Feed Animation
// ===========================
document.getElementById("videoFeed").onerror = function() {
    this.setAttribute('data-loading', 'true');
};

// ===========================
// Key Press Logic
// ===========================
document.addEventListener('DOMContentLoaded', (event) => {
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
});

function handleKeyDown(event) {
    let keyMappings = {
        'ArrowLeft': ['left', 'keyA'],
        'ArrowUp': ['forward', 'keyW'],
        'ArrowRight': ['right', 'keyD'],
        'ArrowDown': ['backward', 'keyS'],
        'w': ['forward', 'keyW'],
        'a': ['left', 'keyA'],
        's': ['backward', 'keyS'],
        'd': ['right', 'keyD']
    };

    if (keyMappings[event.key]) {
        let [direction, elementId] = keyMappings[event.key];
        document.getElementById(elementId).classList.add('active');
        sendCommand(direction);
    }
}

function handleKeyUp(event) {
    let keys = ['ArrowLeft', 'ArrowUp', 'ArrowRight', 'ArrowDown', 'w', 'a', 's', 'd'];

    if (keys.includes(event.key)) {
        sendCommand('stop');
        let elementId = 'key' + event.key.toUpperCase();
        document.getElementById(elementId).classList.remove('active');
    }
}

// ===========================
// Send Command Logic
// ===========================
function sendCommand(direction) {
    console.log(`Sending command: ${direction}`);
    fetch("/command", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'direction': direction })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error sending command:', error));
}

// ===========================
// Gamepad Logic
// ===========================
window.addEventListener("gamepadconnected", function() {
    console.log("Gamepad connected!");
    gamepadInterval = setInterval(checkGamepad, 100); // Check every 100ms
});

window.addEventListener("gamepaddisconnected", function() {
    console.log("Gamepad disconnected!");
    clearInterval(gamepadInterval);
});

function checkGamepad() {
    let gamepads = navigator.getGamepads();
    if (gamepads[0]) {
        let gp = gamepads[0];

        handleJoystickMovement(gp.axes[0], gp.axes[1], 'moveStick');
        handleJoystickMovement(gp.axes[2], gp.axes[3], 'cameraStick');

        handleGamepadButtons(gp.buttons);
    }
}

function handleJoystickMovement(xAxis, yAxis, elementId) {
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

    let stickElement = document.getElementById(elementId);
    if (stickElement) {
        stickElement.style.transform = `translate(-50%, -50%) translate(${xAxis * 40}px, ${yAxis * 40}px)`;
    } else {
        console.error(`${elementId} element not found.`);
    }
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
            sendCommand(mapping.command);
        } else {
            buttonElement.classList.remove('active');
        }
    });
}