var joystick;
var speedStick;

function setupUI()
{
	var joystickCanvas = document.getElementById("joystick");
	var speedCanvas = document.getElementById("speedJoystick");

	//Taking care of the joystick canvas
	//joystickCanvas.height = window.outerHeight;
	//joystickCanvas.width = window.outerWidth / 2;

	//speedCanvas.height = window.outerHeight;
	//speedCanvas.width = window.outerWidth / 2;

	joystick = new JoystickProt("joystick", 0, 1, 0, 1, 200, 200);
	speedStick = new JoystickProt("speedJoystick", 0, 1, 0, 1, 200, 200);
}