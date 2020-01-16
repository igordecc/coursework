export default function draw_edge(ctx, location1, location2){
    ctx.save()
    ctx.lineWidth = '3';
    ctx.strokeStyle = 'rgb(117, 26, 255)'
    ctx.beginPath();
    ctx.moveTo(location1.x, location1.y);
    ctx.lineTo(location2.x, location2.y)
    ctx.stroke();
    ctx.restore()
}