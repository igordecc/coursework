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
                console.log("this is colection data",collectedData)
                console.log("this is metadata,",event.data)
                break;
            case "iteration":
                //console.log("this is iterations data",event.data);
                break;
            } 
        }
    }