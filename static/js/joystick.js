function JoystickProt(elementID, minValX, maxValX, minValY, maxValY, width, height)
{
	this.element = document.getElementById(elementID);

	this.ctx = this.element.getContext("2d");

	this.elementBounds = this.element.getBoundingClientRect();

	this.touchID = -1;

	this.centerX = 0
	this.centerY = 0

	this.offsetX = 0; //The current y offset of the joystick
	this.offsetY = 0;

	this.active = false

	this.minValX = minValX;
	this.maxValX = maxValX;
	this.minValY = minValY;
	this.maxValY = maxValY;

	this.width = width;
	this.height = height;

	this.xVal;
	this.yVal;

	this.update = function()
	{
		this.draw();
	}

	this.draw = function()
	{
		this.ctx.clearRect(0, 0, this.element.width, this.element.height);

		if(this.active == true)
		{
			//Drawing a circle
			this.ctx.beginPath();
			this.ctx.arc(this.centerX, this.centerY, this.width / 2, 0, 2 * Math.PI, false)

			this.ctx.lineWidth = 3;
			this.ctx.strokeStyle = "#000000";
			this.ctx.stroke();
			this.ctx.closePath();

			//Also drawing the offset
			this.ctx.beginPath();
			this.ctx.arc(this.centerX + this.offsetX, this.centerY + this.offsetY, 10, 0, 2 * Math.PI, false);
			this.ctx.fillStyle = "#333333";
			this.ctx.fill();
			this.ctx.closePath();
		}
	}

	this.calculateValue = function()
	{
		var edgeX = this.centerX - this.width / 2;
		var edgeY = this.centerY - this.height / 2; //0 assumes that the element is at the top of the page

		var edgeOffsetX = edgeX + this.offsetX;
		var edgeOffsetY = edgeY + this.offsetY;

		var xAmount = edgeOffsetX / this.width;
		var yAmount = edgeOffsetY / this.height;

		this.xVal = minValX + maxValX * xAmount;
		this.yVal = minValY + maxValY * yAmount;

		if(this.xVal > this.maxValX)
			this.xVal = this.maxValX;
		if(this.xVal < this.minValX)
			this.xVal = this.minValX;

		if(this.yVal > this.maxValY)
			this.yVal = this.maxValY;
		if(this.yVal < this.minValY)
			this.yVal = this.minValY;
	}

	this.onTouchStart = function(e)
	{
		e.preventDefault();

		if(this.active == false)
		{
			this.active = true;

			this.centerX = e.touches[0].pageX - this.elementBounds.left;
			this.centerY = e.touches[0].pageY - this.elementBounds.top;

			this.touchID = e.touches[0].identifier;
			
			this.offsetX = 0;
			this.offsetY = 0;
			this.calculateValue();
		}

		this.update();


		return false;
	}
	this.onTouchMove = function(e)
	{
		e.preventDefault();

		//Going thru all the touches
		for(var i = 0; i < e.touches.length; i++)
		{
			if(this.active == true && this.touchID == e.touches[i].identifier)
			{
				//Calculating the touch position relative to the element
				var posX = e.touches[i].pageX - this.elementBounds.left;
				var posY = e.touches[i].pageY - this.elementBounds.top;

				this.offsetX = posX - this.centerX;
				this.offsetY = posY - this.centerY;

				//console.log("X: " + this.offsetX + " Y: " + this.offsetY);

				this.calculateValue();
			}
		}

		this.update();

		return false;
	}
	this.onTouchEnd = function(e)
	{
		e.preventDefault();

		//Going thru all the touches
		for(var i = 0; i < e.changedTouches.length; i++)
		{
			if(this.active == true && this.touchID == e.changedTouches[i].identifier)
			{
				this.active = false;

				this.offsetX = 0;
				this.offsetY = 0;
			}
		}

		this.update();

		return false;
	}

	//this.element.ontouchstart = function(e)
	//Set the event listeners to the elements, bind this to make "this" inside the function point to the prototype
	this.element.addEventListener("touchstart", this.onTouchStart.bind(this), false); 

	//this.element.ontouchmove = function(e)
	this.element.addEventListener("touchmove", this.onTouchMove.bind(this), false);

	//this.element.ontouchend = function(e)
	this.element.addEventListener("touchend", this.onTouchEnd.bind(this), false);
}