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
function draw_circle(ctx, location, colour) {
  ctx.save();
  ctx.fillStyle = 'rgb(255, 51, 204)'
  ctx.shadowColor = 'dodgeblue'
  ctx.shadowBlue = 20   
  ctx.scale(SCALE, SCALE)
  ctx.translate(location.x / SCALE - OFFSET, location.y / SCALE - OFFSET)
  ctx.beginPath();
  ctx.arc(100, 75, 50, 0, 2 * Math.PI);
  //ctx.fillStyle = 'rgb(255, 51, 204)';
  ctx.fillStyle = colour;
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

// ----------hooks-----------
// hook is a data managing function
function usePersistentCanvas(data) {
  const [locations, setLocations] = usePersistentState([], 'draw-app')
  const canvasRef = React.useRef(null)
  var [colorList, setColorList] = usePersistentState([],'color-list')

  // update canvas
  React.useEffect(() => {
    // delay
    let timeout = 1000
    setTimeout(() => {}, timeout);

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    
    // create default color list
    function create_default_color_list(){
      let colour_list = []
      for (let location in locations) {
        let new_colour = data.phase_vector[0][location]*50
        colour_list.push(`hsl(300, 100%, 50%)`) //max 360
      }  
      return colour_list
    }

    // zip
    function zip_locations_and_color_list(colour_list){
      let zipped = []
      for (let location in locations) {
        zipped.push([locations[location], colour_list[location]])
      }
      return zipped
    }

    function draw_all(zipped, screen_lines){
      zipped.forEach((l_and_c) => draw_circle(ctx, l_and_c[0], l_and_c[1]))
      screen_lines.forEach(line => draw_line(ctx, line))
    }

    let colour_list = create_default_color_list()
    let zipped = zip_locations_and_color_list(colour_list)
    draw_all(zipped, screen_lines)

    // dont use setColorList(colour_list)
    // set up color other way or reed how to work useEffect
  })
  
  
  return [locations, setLocations, canvasRef, colorList, setColorList]
}

// set data hook
function usePersistentData(init){
  const [data, setData] = usePersistentState(init, 'osc-data')
  
  return [data, setData]
}

// -------------------------------

// Application render function
function App() {
  // states
  const [data, setData] = usePersistentData({});
  const [locations, setLocations, canvasRef, colorList, setColorList] = usePersistentCanvas(data);
  

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
    // reload everything - all app

    function fetch_data() {
      // connection to server
      fetch(DataURL).           
      then(result => result.json()).
      then(e => {
        setData(e);
      }).
      catch(error => console.log(error))
      //console.log(data)
    }
    
    function define_data_params(){
        // main parameters
      oscillators_number = _.size(data.Aij[0])
      group_number = _.size(data.community_list)
      //console.log(oscillators_number, group_number)
    }

    
    function divide_screen(){
      // dividing screen acording to group size
      // var screen_lines = []  // at the constants
      let vertical_line = 0
      screen_lines = []
      for (let i=0; i < group_number; i++) {
        let community_size = _.size(data.community_list[i])
        vertical_line += window.innerWidth * (community_size / oscillators_number) 
        screen_lines.push( vertical_line )
      }
      //console.log("screen lines:", screen_lines)
    }


    function calculate_osc_locations() {
      // return locations
      let _locations = []
      function rand_normal() {
        // random normal distribution [0 ; 1]
        var u = 0, v = 0;
        while(u === 0) u = Math.random(); //Converting [0,1) to (0,1)
        while(v === 0) v = Math.random();
        let num = Math.sqrt( -2.0 * Math.log( u ) ) * Math.cos( 2.0 * Math.PI * v );
        num = num / 10.0 + 0.5; // Translate to 0 -> 1
        if (num > 1 || num < 0) return rand_normal(); // resample between 0 and 1
        return num;
      }

      let _previous_line = 0
      let community_list = data.community_list

      for (let _line in community_list) {     
      let _line_coordinate = screen_lines[_line]
        for (let _oscillator in community_list[_line]) {

          let randomX = _previous_line + (rand_normal()*(_line_coordinate - _previous_line))  // random between sertain screen_lines
          let randomY = (rand_normal()*window.innerHeight)  // random between sertain screen_lines
          
          let newLocation = {x: randomX, y: randomY}
          _locations.push(newLocation)
        }
        _previous_line += _line_coordinate
      }  
      return _locations
    }


    fetch_data()
    define_data_params()
    divide_screen()
    setLocations(calculate_osc_locations())
    //console.log(locations)
  }

  function handlerStartEvaluation(){
    let color_list = []
    for (let location in locations) {
      let color = data.phase_vector[0][location]*100
      let hsl_color = `hsl(${color},100%,50%)`
      color_list.push(hsl_color)
    }
    setColorList([color_list])
    console.log(color_list )
    console.log(colorList)
  }

  function handlerStopEvaluation(){

  }

  function handlerChangeEvaluationSpeed(){

  }
  // render
  return (
    <> 
      <div className="controls">
        <button onClick={handleClear}>Clear</button>
        <button onClick={handleUndo}>Undo</button>
        <button onClick={handleReloadOscillatorsData}>Reload</button>
        <button onClick={handlerStartEvaluation}>Start</button>
        <button onClick={handlerStopEvaluation}>Stop</button>
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
