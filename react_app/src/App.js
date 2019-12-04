import React from 'react';

// canvas simple example
// created from w3c canvas tutorial and https://itnext.io/using-react-hooks-with-canvas-f188d6e416c0
// create simple canvas using useRef React hook

const DataURL = `http://localhost:5000/`
const SCALE = 0.3
const OFFSET = 80

function draw_circle(ctx, location) {
  ctx.save()
  ctx.fillStyle = 'rgb(255, 51, 204)'
  ctx.shadowColor = 'dodgeblue'
  ctx.shadowBlue = 20   
  ctx.save()
  ctx.scale(SCALE, SCALE)
  ctx.translate(location.x / SCALE - OFFSET, location.y / SCALE - OFFSET)
  ctx.beginPath();
  ctx.arc(100, 75, 50, 0, 2 * Math.PI);
  ctx.fillStyle = 'rgb(255, 51, 204)';
  ctx.fill();
  ctx.stroke();
  ctx.restore()
}

// custom hook
function usePersistentState(init) {
  const [value, setValue] = React.useState(
    JSON.parse(localStorage.getItem('draw-app')) || init
  )
  React.useEffect(() => {
    localStorage.setItem('draw-app', JSON.stringify(value))
  })
  return [value, setValue]
}

  // our second custom hook: a composition of the first custom hook
  function usePersistentCanvas() {
    const [locations, setLocations] = usePersistentState([])

    const canvasRef = React.useRef(null)

    React.useEffect(() => {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
      locations.forEach(location => draw_circle(ctx, location))
    })
    return [locations, setLocations, canvasRef]
  }

// load and save server Data to local storage 
function usePersistentData(init){
  const [data, setData] = React.useState(
    JSON.parse(localStorage.getItem('osc-data')) || init
  )
  React.useEffect(() => {
    localStorage.setItem('osc-data', JSON.stringify(data))
  })
  return [data, setData]
}

function App() {

  const [locations, setLocations, canvasRef] = usePersistentCanvas([])
  const [data, setData] = usePersistentData({});

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
    
    fetch(DataURL).
    then(result => result.json()).
    then(e => (setData(e))).
    catch(error => console.log(error))
    console.log(data)
  }
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
