//Loosely adapted from
//http://codetheory.in/html5-canvas-drawing-lines-with-smooth-edges/
//Using his "moveTo" idea gave me the best balance between responsiveness and
//smoothness. Suggested algorithm for "quadraticCurveTo" caused me some issues.
//TODO: This probably isn't touch screen friendly at the moment.
$(function() {
    var canvas = document.querySelector("#canvas");
    var ctx = canvas.getContext("2d");

    var mouse = {x: 0, y: 0};
    var last_mouse = {x: 0, y: 0};
    
    /* Mouse Capturing Work */
    canvas.addEventListener("mousemove", function(e) {
        last_mouse.x = mouse.x;
        last_mouse.y = mouse.y;
        
        mouse.x = e.pageX - this.offsetLeft;
        mouse.y = e.pageY - this.offsetTop;
    }, false);
    
    /* Drawing on Paint App */
    ctx.lineWidth = 5;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.strokeStyle = "darkblue";
    
    canvas.addEventListener("mousedown", function(e) {
        canvas.addEventListener("mousemove", onPaint, false);
    }, false);
    
    canvas.addEventListener("mouseup", function() {
        canvas.removeEventListener("mousemove", onPaint, false);
    }, false);
    
    var onPaint = function() {
        ctx.beginPath();
        ctx.moveTo(last_mouse.x, last_mouse.y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.closePath();
        ctx.stroke();
    };

    $("#clear_btn").click(function() {
        ctx.clearRect(0,0,canvas.width, canvas.height);
    });
});
