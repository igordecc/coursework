/*
Application module. Compile results of all other scripts and prepairs files for render.
*/ 

import React from 'react';
import {usePersistentData, usePersistentCanvas} from  './hooksLib';
import {Clear, Undo, Reload, Start, Stop} from './components/buttons';
var _ = require('underscore');
const DataURL = `http://localhost:5000/`


var oscillators_number = 0
var group_number = 0


// Application render function
function App() {
  // states
  const [data, setData] = usePersistentData({});
  const [locations, setLocations, canvasRef, colorList, setColorList, screen_lines, setScreenLines] = usePersistentCanvas(data);
  

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
      let vertical_line = 0
      var _screen_lines = []
      for (let i=0; i < group_number; i++) {
        let community_size = _.size(data.community_list[i])
        vertical_line += window.innerWidth * (community_size / oscillators_number) 
        _screen_lines.push( vertical_line )
      }
      return _screen_lines;
      
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
        let _difference = _line_coordinate - _previous_line
          for (let _oscillator in community_list[_line]) {
            
            let randomX = _previous_line + (rand_normal()*(_difference))  // random between sertain screen_lines
            let randomY = (rand_normal()*window.innerHeight)  // random between sertain screen_lines
            
            let newLocation = {x: randomX, y: randomY}
            _locations.push(newLocation)
          }
        _previous_line += _difference
        }  
      return _locations
    }


    fetch_data()
    define_data_params()
    setScreenLines(divide_screen()) 
    setLocations(calculate_osc_locations())
    //console.log(locations)
  }

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
      for (let vector in data.phase_vector) {
        
        // sleep on each iteration
        let color_list = []
        await sleep(delay||1000).then(() => {
          for (let location in locations) {  // change colors of dots
            let color = data.phase_vector[vector][location]*100
            let hsl_color = `hsl(${color},100%,50%)`
            color_list.push(hsl_color)
          }
        })
        

        setColorList(color_list)
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
        <button onClick={handleClear}>Clear</button>
        <button onClick={handleUndo}>Undo</button>
        <button onClick={handleReloadOscillatorsData}>Reload</button>
        <button onClick={handlerStartEvaluation}>Start</button>
        <button onClick={handlerStopEvaluation}>Stop</button>
        <Clear/>
        <Undo/>
        <Reload/>
        <Start/>
        <Stop/>
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
