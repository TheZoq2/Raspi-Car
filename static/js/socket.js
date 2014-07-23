var connection;

function setupSocket()
{
	var ip = 'ws://192.168.1.77:8888/websocket'
	connection = new WebSocket(ip, ['soap', 'xmpp']);

	connection.onopen = function()
	{
		connection.send('Ping:Ping'); //:Ping because all messages are parsed 
	}
	connection.onerror = function (error)
	{
		console.log('WebSocket error: ' + error);
	}
	connection.onmessage = function(message)
	{
		console.log("Socket message: ", message.data);
	}
}

function sendMessage(msg)
{
	connection.send(msg)
}