// canvas draw circle functions
function draw_circle(ctx, location, color) {
    const SCALE = 0.3
    const OFFSET = 80

    ctx.save();
    ctx.fillStyle = 'rgb(255, 51, 204)'
    ctx.shadowColor = 'dodgeblue'
    ctx.shadowBlue = 20   
    ctx.scale(SCALE, SCALE)
    ctx.translate(location.x / SCALE - OFFSET, location.y / SCALE - OFFSET)
    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.arc(100, 75, 50, 0, 2 * Math.PI);
    //ctx.fillStyle = 'rgb(255, 51, 204)';
    ctx.fill();
    ctx.stroke();
    ctx.restore();
  }
  
  export default draw_circle;