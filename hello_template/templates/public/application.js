$(window).on('load', function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];
	console.log("Anshul beginning")
	console.log(document.domain)
	console.log(location.port)
    //receive details from server
    socket.on('newnumber', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        //if (numbers_received.length >= 10){
        //    numbers_received.shift()
        //}            
		console.log("Anshul message is" + msg)
        numbers_received.push(msg.number);
		console.log("Anshul pushed message")
		console.log(numbers_received.length)
        numbers_string = '';
        for (var i = 0; i < numbers_received.length; i++){
			console.log("Anshul in loop")
            numbers_string = numbers_string + '<p>' + numbers_received[0].toString() + '</p>';
        }
		console.log("Anshul after loop before updating html")
		var temp = document.getElementById("dynamicResults")
		console.log("Anshul the id is" + temp)
        temp.innerHtml = numbers_string;
		console.log("Anshul after updating html")
    });

});