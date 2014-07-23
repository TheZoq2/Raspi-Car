function setupRobot()
{
	setInterval(updateRobot, 100);
}
function updateRobot()
{
	//Turning based on the joystick
	if(joystick.active == true)
	{
		sendTurnCommand(joystick.xVal);
	}

	if(speedStick.active == true)
	{
		sendDirCommand(speedStick.yVal);
	}
	else
	{
		sendDirCommand(0.5);
	}
}

function sendDirCommand(dir)
{
	sendMessage("driveDir:" + dir)
}
function sendTurnCommand(amount)
{
	sendMessage("turnAmount:" + amount)
}