/*
Application module. Compile results of all other scripts and prepairs files for render.
*/ 

import React from 'react';
import {usePersistentData, usePersistentCanvas, useAllData} from  './hooksLib';
import {Clear, Undo, Reload, Start, Stop} from './components/buttons';
import {draw_circle, draw_v_line} from './drawLib'
import {handleCanvasClick, handleClear, handleUndo, handleReload, handleStart, handleStop} from './logic';
var _ = require('underscore');
const DataURL = `http://localhost:5000/`


var oscillators_number = 0
var group_number = 0


// Application render function
function App() {
  // states
  const props = useAllData();
  const canvasRef = React.useRef(null)
  //console.log('locations')
  

  // update canvas
  React.useEffect(() => {

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    

    function draw_all(zipped, screen_lines){
      zipped.forEach((l_and_c) => draw_circle(ctx, l_and_c[0], l_and_c[1]))
      screen_lines.forEach(line => draw_v_line(ctx, line))
    }
    
    draw_all(props.zipped, props.screenLines)

    // dont use setColorList(colour_list)
    // set up color other way or reed how to work useEffect
  })

  // TODO: line
  // TODO: update lines with useEffect


    function handlerChangeEvaluationSpeed(){

  }
  // render
  return (
    <> 
      <div className="controls">  
        <Clear onClick={e=>{handleClear(props)}}/>
        <Undo onClick={e=>{handleUndo(props)}}/>
        <Reload onClick={e=>{handleReload(props)}}/>
        <Start onClick={e=>{handleStart(props)}}/>
        <Stop onClick={e=>{handleStop(props)}}/>
      </div>
      <canvas 
        ref={canvasRef}
        width={window.innerWidth}
        height={window.innerHeight}
        onClick={e=>{
          e.props = props
          handleCanvasClick(e)
        }} 
      />
    </>
  );
}

export default App;
