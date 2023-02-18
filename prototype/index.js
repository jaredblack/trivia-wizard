
function submitJoin() {
    const websocket = new WebSocket(getWebSocketServer());

    websocket.addEventListener("open", () => {
        const joinId = document.querySelector("#joinInput").value;
        const event = {
            type: "init",
            joinId: joinId,
        }
        console.log("sending event: " + JSON.stringify(event));
        websocket.send(JSON.stringify(event));
    });
    submitAnswer(websocket);
}

function submitAnswer(websocket) {
    const answerButton = document.querySelector("#answerButton");
    answerButton.addEventListener("click", () => {
        const answer = document.querySelector("#answerInput").value;
        const event = {
            type: "answer",
            answer: answer
        }
        websocket.send(JSON.stringify(event));
    });
}

function getWebSocketServer() {
    if (window.location.host ==="jaredblack.github.io") {
        return "wss://triviawizard.herokuapp.com";
    } else if (window.location.host === "localhost:5500"){
        return "ws://localhost:8001";
    } else {
        throw new Error(`Unsupported host: ${window.location.host}`);
    }
}
