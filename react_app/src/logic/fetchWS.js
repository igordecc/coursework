export default async function fetchWS(){
    let url = "ws://localhost:1234/"
    console.log("KILROY WAS HERE")
    var myWebSocket = new WebSocket(url)
    myWebSocket.onopen = function sendMessage() {
        for (let i=0; i < 10000; i++) {
            setTimeout(
                myWebSocket.send("its "+i.toString()+" second"),
                10000 // 1 second
                )
    }
    
    
    
        
    }
}