import React from 'react';
var _ = require('underscore');
// canvas simple example
// created from w3c canvas tutorial and https://itnext.io/using-react-hooks-with-canvas-f188d6e416c0
// create simple canvas using useRef React hook
// TODO: infuse lines with magnetta color
// TODO: bind draw lines with reaload function (also use screen_lines list)

const DataURL = `http://localhost:5000/`
const SCALE = 0.3
const OFFSET = 80

// canvas draw functions
function draw_circle(ctx, location) {
  ctx.save();
  ctx.fillStyle = 'rgb(255, 51, 204)'
  ctx.shadowColor = 'dodgeblue'
  ctx.shadowBlue = 20   
  ctx.scale(SCALE, SCALE)
  ctx.translate(location.x / SCALE - OFFSET, location.y / SCALE - OFFSET)
  ctx.beginPath();
  ctx.arc(100, 75, 50, 0, 2 * Math.PI);
  ctx.fillStyle = 'rgb(255, 51, 204)';
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

function draw_line(ctx, xlocation) {
  //location = x
  ctx.save();
  ctx.moveTo(xlocation, 0);
  ctx.lineTo(xlocation, window.innerHeight)
  ctx.stroke();
  ctx.restore();
}

// data cashing hook
function usePersistentState(init, itemName='') {
  const [value, setValue] = React.useState(
    JSON.parse(localStorage.getItem(itemName)) || init
  )
  React.useEffect(() => {
    localStorage.setItem(itemName, JSON.stringify(value))
  })
  return [value, setValue]
}

// set canvas hook 
// hook is a data managing function
function usePersistentCanvas() {
  const [locations, setLocations] = usePersistentState([], 'draw-app')

  const canvasRef = React.useRef(null)

  // update canvas
  React.useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    locations.forEach(location => draw_circle(ctx, location))
  })
  return [locations, setLocations, canvasRef]
}

// set data hook
function usePersistentData(init){
  const [data, setData] = usePersistentState(init, 'osc-data')
  
  return [data, setData]
}

// set locations hook
function usePersistentRandomLocations(init) {
  const [locations, setLocations] = usePersistentState(init, 'osc-locations')
  
  return [locations, setLocations]
}

// Application render function
function App() {
  // states
  const [locations, setLocations, canvasRef] = usePersistentCanvas([]);
  const [data, setData] = usePersistentData({});
  const [oscNumber, setOscNumber] = React.useState(null);
  const [randomLocations, setRandomLocations] = usePersistentRandomLocations([]);

  // handlers
  function handleCanvasClick (e) {
    const newLocation = {x: e.clientX, y: e.clientY}
    setLocations([...locations, newLocation])
  }

  function handleClear() {
    setLocations([])
  }

  function handleUndo (){
    setLocations(locations.slice(0,-1))
  }

  function handleReloadOscillatorsData (){  
    // connection to server
    fetch(DataURL).           
    then(result => result.json()).
    then(e => {
      setData(e);
    }).
    catch(error => console.log(error))
    console.log(data)

    // main parameters
    let oscillators_number = _.size(data.Aij[0])
    let group_number = _.size(data.community_list)

    // dividing screen acording to group size
    let screen_lines = []
    let vertical_line = 0
    for (let i=0; i < group_number-1; i++) {
      console.log(i)
      let community_size = _.size(data.community_list[i])
      vertical_line += window.innerWidth * (community_size / oscillators_number) 
      screen_lines.push( vertical_line )
    }
    console.log(screen_lines)
    
  }
  // render
  return (
    <> 
      <div className="controls">
        <button onClick={handleClear}>Clear</button>
        <button onClick={handleUndo}>Undo</button>
        <button onClick={handleReloadOscillatorsData}>Reload</button>
      </div>
      <canvas 
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight}
        onClick={handleCanvasClick} 
      />
    </>
  );
}

export default App;
