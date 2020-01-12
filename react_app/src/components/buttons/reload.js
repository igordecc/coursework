import React from 'react';
const _ = require('underscore');

export default function reload(){

    /* function handleReloadOscillatorsData (){  
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
      } */

    // return <button onClick={handleReloadOscillatorsData}>Reload</button>
    return <button>Reload I M HERE</button>
};