import React from 'react';
// canvas simple example
// created from w3c canvas tutorial and https://itnext.io/using-react-hooks-with-canvas-f188d6e416c0
// create simple canvas using useRef React hook




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

function App() {
  const canvasRef = React.useRef(null)
  const [locations, setLocations] = usePersistentState([])
  console.log(locations)

  React.useEffect( () => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    locations.forEach(location => draw_circle(ctx, location))
  })

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

  

  // our second custom hook: a composition of the first custom hook
  function usePersistentCanvas() {
    const [locations, setLocation] = usePersistentState([])

    const canvasRef = React.useRef(null)

    React.useEffect(() => {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')
      ctx.clearReact(0, 0, window.innerWidth, window.innerHeight)
      locations.forEach(location => draw_circle(ctx, location))
    })
    return [locations, setLocations, canvasRef]
  }

  return (
    <> 
      <div className="controls">
        <button onClick={handleClear}>Clear</button>
        <button onClick={handleUndo}>Undo</button>
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
