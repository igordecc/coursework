export default function handleCanvasClick(e){
    const newLocation = {x: e.clientX, y: e.clientY}
    e.setLocations([...e.locations, newLocation])
}