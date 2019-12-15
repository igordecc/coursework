import React from 'react';
var _ = require('underscore');
// canvas simple example
// created from w3c canvas tutorial and https://itnext.io/using-react-hooks-with-canvas-f188d6e416c0
// create simple canvas using useRef React hook


const DataURL = `http://localhost:5000/`
const SCALE = 0.3
const OFFSET = 80

var oscillators_number = 0
var group_number = 0
var screen_lines = []

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
  ctx.lineWidth = '5';
  ctx.strokeStyle = 'rgb(117, 26, 255)'
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
    screen_lines.forEach(line => draw_line(ctx, line))
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
    oscillators_number = _.size(data.Aij[0])
    group_number = _.size(data.community_list)

    // dividing screen acording to group size
    // var screen_lines = []  // at the constants
    let vertical_line = 0
    screen_lines = []
    for (let i=0; i < group_number; i++) {
      let community_size = _.size(data.community_list[i])
      vertical_line += window.innerWidth * (community_size / oscillators_number) 
      screen_lines.push( vertical_line )
    }
    console.log("screen lines:", screen_lines)
    
    // random normal distribution [0 ; 1]
    function rand_normal() {
      var u = 0, v = 0;
      while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
      while(v === 0) v = Math.random();
      let num = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
      num = num / 10.0 + 0.5; // Translate to 0 -> 1
      if (num > 1 || num < 0) return rand_normal(); // resample between 0 and 1
      return num;
    }

    var calculate_oscillators = function () {
      // for let _line in screen_lines
      //for (let line_number=0; line_number < _.size(screen_lines); line_number++) {      
        let _previous_line = 0
        let community_list = data.community_list
        for (let _line in community_list) {     
        let _line_coordinate = screen_lines[_line]
          for (let _oscillator in community_list[_line]) {
            
            console.log("screen line: ", screen_lines[_line])
            console.log(_line_coordinate - _previous_line)
            let randomX = _previous_line + (rand_normal()*(_line_coordinate - _previous_line))  // random between sertain screen_lines
            let randomY = (rand_normal()*window.innerHeight)  // random between sertain screen_lines
            
            let newLocation = {x: randomX, y: randomY}
            locations.push(newLocation)
          }
        _previous_line += _line_coordinate
      }  
    }

    calculate_oscillators()
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
