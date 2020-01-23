/*
Application module. Compile results of all other scripts and prepairs files for render.
*/ 

import React from 'react';
import {usePersistentData, usePersistentCanvas, useAllData} from  './hooksLib';
import {DefaultButton, Undo, Reload, Start, Stop, StartWS} from './components/buttons';
import {draw_circle, draw_v_line, draw_edge} from './drawLib'
import {handleCanvasClick, handleClear, handleUndo, handleReload, handleStart, handleStop, handleEvaluationWS} from './logic';
var _ = require('underscore');
const DataURL = `http://localhost:5000/`


var oscillators_number = 0
var group_number = 0


// Application render function
function App() {
  
  // states
  const props = useAllData();
  //console.log(props.data)
  //console.log(props)
  const canvasRef = React.useRef(null)

  // update canvas
  
  React.useEffect(() => {

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.clearRect(0, 0, window.innerWidth, window.innerHeight)
    

    function draw_all(zipped, screen_lines){
      zipped.forEach((l_and_c) => draw_circle(ctx, l_and_c[0], l_and_c[1]))
      //screen_lines.forEach(line => draw_v_line(ctx, line))
    }

    let edge_list = props.data.node_edges
    /*Always check if array is empty, or else it will try to render empty array and fail gacefuly.*/
    if (Array.isArray(props.locations)&&props.locations.length){
      for (let edge in edge_list) {
        draw_edge(ctx, props.locations[edge_list[edge][0]], props.locations[edge_list[edge][1]])
      }
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
        <DefaultButton onClick={e=>{handleClear(props)}} buttonLable='Clear'/>
        <DefaultButton onClick={e=>{handleUndo(props)}} buttonLable='Undo'/>
        <DefaultButton onClick={e=>{handleReload(props)}} buttonLable='Reload'/>
        <DefaultButton onClick={e=>{handleStart(props)}} buttonLable='Start'/>
        <DefaultButton onClick={e=>{handleStop(props)}} buttonLable='Stop'/>
        <DefaultButton onClick={e=>{handleEvaluationWS(props)}} buttonLable='StartWS'/>
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
