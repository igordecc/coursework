export default function handlerStartEvaluation(props){
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
