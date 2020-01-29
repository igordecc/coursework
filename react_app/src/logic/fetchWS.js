export default async function fetchWS(props){
    let url = "ws://localhost:1234/"
    var myWebSocket = new WebSocket(url)
    myWebSocket.onopen = function sendMessage() {
                myWebSocket.send("load")    
            }
    var collectedData = {}
    myWebSocket.onmessage = function receiveMessage(event){
        let msg = JSON.parse(event.data)
        switch (msg.type) {
            case "metadata":
                for (let property in msg.metadata){
                    collectedData[property] = msg.metadata[property]
                }
                //console.log("metadata taken")
                break;
                
            case "iteration":
                // add new iteration data to already Collected
                for (let property in msg.iteration_data){
                    collectedData[property] = collectedData[property].concat(msg.iteration_data[property])
                }
                // update dynamic states, by overriding it
                for (let property in msg.dynamic_states){
                    collectedData[property] = msg.dynamic_states[property]
                }
                //console.log("iteration data taken");
                break;
        } 
        props.setData(collectedData)
    }
    
}