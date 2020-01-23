import React, {useState} from 'react';
import usePersistentState from './usePersistentState';
import draw_v_line from '../drawLib/drawVLine'
import draw_circle from '../drawLib/drawCircle'

function usePersistentCanvas(data) {
    const [locations, setLocations] = usePersistentState([], 'draw-app')
    const [screen_lines, setScreenLines] = useState([]);
    //var [colorList, setColorList] = usePersistentState([],'color-list')
  
      // create default color list
      function create_default_color_list(){
        let colour_list = []
        for (let location in locations) {
          let new_colour = data.phase_vector[0][location]*50
          colour_list.push(`hsl(${new_colour}}, 100%, 50%)`) //max 360
        }  
        return colour_list
      }
  
      // zip
      function zip_locations_and_color_list(colour_list){
        let zipped = []
        for (let i=0; i<locations.length; i++) {
          //console.log([locations[i], colour_list[0][i]])
          zipped.push([locations[i], colour_list[i]])
        }
        return zipped
      }
  
      
      
      let colour_list = []//create_default_color_list()
      var [colorList, setColorList] = usePersistentState(colour_list,'color-list')
      let zipped = zip_locations_and_color_list(colorList)
  
  

        
    return [locations, setLocations, zipped, colorList, setColorList, screen_lines, setScreenLines]
  }

  export default usePersistentCanvas;