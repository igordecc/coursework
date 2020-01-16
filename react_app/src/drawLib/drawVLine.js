function draw_v_line(ctx, xlocation) {

  ctx.lineWidth = '5';
  ctx.strokeStyle = 'rgb(117, 26, 255)'

  ctx.beginPath();
  ctx.moveTo(xlocation, 0);
  ctx.lineTo(xlocation, window.innerHeight)
  ctx.stroke();
  
  //ctx.restore()
}

export default draw_v_line;