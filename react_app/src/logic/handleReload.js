import React from 'react';

var _ = require('underscore');
const DataURL = `http://localhost:5000/`

var oscillators_number = 0
var group_number = 0

export default function handleReload(props){  
    // reload everything - all app

    function fetch_data() {
      // connection to server
      fetch(DataURL).           
      then(result => result.json()).
      then(e => {
        props.setData(e);
      }).
      catch(error => console.log('ERROR: ', error))
      //console.log("props data: ",props.data)
    }
    
    function define_data_params(){
        // main parameters
      oscillators_number = _.size(props.data.phase_vector[0])
      group_number = _.size(props.data.community_list)
      //console.log(oscillators_number, group_number)
    }

    
    function divide_screen(){
      // dividing screen acording to group size
      let vertical_line = 0
      var _screenLines = []
      for (let i=0; i < group_number; i++) {
        let community_size = _.size(props.data.community_list[i])
        vertical_line += window.innerWidth * (community_size / oscillators_number) 
        _screenLines.push( vertical_line )
      }
      return _screenLines;
      
    }



    function calculate_osc_locations() {
      // rescale data coordinates from absolute to screen size
      let xy_list = props.data.nodes_coordinates
      let coordinates = []
      let x = 0
      let y = 0
      for (let i=0; i< xy_list.length; i++) {
        x = (xy_list[i][0]+1.2) * window.innerWidth/2.5    
        y = (xy_list[i][1]+1.2) * window.innerHeight/2.5  
        coordinates.push({'x':x, 'y':y})
      }  
      return coordinates
    }


    fetch_data()
    define_data_params()
    props.setScreenLines(divide_screen()) 
    props.setLocations(calculate_osc_locations())
    //console.log(locations)
  } 