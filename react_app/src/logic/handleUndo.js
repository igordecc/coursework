export default function handleUndo(props){
    props.setLocations(props.locations.slice(0, -1))
}