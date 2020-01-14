export default function handleUndo(e){
    e.setLocations(e.locations.slice(0, -1))
}