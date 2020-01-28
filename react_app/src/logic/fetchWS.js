export default async function fetchWS(){
    let url = "ws://localhost:1234/"
    console.log("KILROY WAS HERE")
    var myWebSocket = new WebSocket(url)
    myWebSocket.onopen = function sendMessage() {
                myWebSocket.send("load")
            }
        }