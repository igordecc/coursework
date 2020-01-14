export default function handleCanvasClick(e){
    const newLocation = {x: e.clientX, y: e.clientY}
    e.props.setLocations([...e.props.locations, newLocation])
}