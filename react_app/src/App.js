/*
Application module. Compile results of all other scripts and prepairs files for render.
*/ 

import React from 'react';
import {usePersistentData, usePersistentCanvas, useAllData} from  './hooksLib';
import {Clear, Undo, Reload, Start, Stop} from './components/buttons';
import {draw_circle, draw_v_line} from './drawLib'
import {handleCanvasClick, handleClear, handleUndo, handleReload} from './logic';
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


  // handlers

  

  function handlerStartEvaluation(){
    let timeout = 100 

    const sleep = (milliseconds) => {
      return new Promise(resolve => setTimeout(resolve, milliseconds))
    }
    

    const doWithDelay = async (delay) => {
      await sleep(delay||1000)
      //do stuff
    }
    
    
    async function evaluate(delay) {
      for (let vector in props.data.phase_vector) {
        
        // sleep on each iteration
        let color_list = []
        await sleep(delay||1000).then(() => {
          for (let location in props.locations) {  // change colors of dots
            let color = props.data.phase_vector[vector][location]*100
            let hsl_color = `hsl(${color},100%,50%)`
            color_list.push(hsl_color)
          }
        })
        

        props.setColorList(color_list)
        //console.log(color_list )
        //console.log(colorList)
      }
    }
    evaluate(timeout)
  }

  function handlerStopEvaluation(){

  }

  function handlerChangeEvaluationSpeed(){

  }
  // render
  return (
    <> 
      <div className="controls">
        <button onClick={e=>{handleClear(props)}}>Clear</button>
        <button onClick={e=>{handleUndo(props)}}>Undo</button>
        <button onClick={e=>{handleReload(props)}}>Reload</button>
        <button onClick={handlerStartEvaluation}>Start</button>
        <button onClick={handlerStopEvaluation}>Stop</button>
        <Clear/>
        <Undo/>
        <Reload onClick={e=>{handleReload(props)}}/>
        <Start/>
        <Stop/>
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
