function submitCreate() {
    const joinId = document.querySelector('#textCreateJoin').value;
    console.log(joinId);
    const websocket = new WebSocket(getWebSocketServer());
    // initSocket(websocket, joinId);
    websocket.addEventListener("open", () => {
        const event = {
            type: "init",
            joinId: joinId,
            create: true,
        };
        websocket.send(JSON.stringify(event));
    });
    doSomething(websocket);
    receiveAnswers(websocket);
}

function initSocket(websocket, joinId) {

}

function receiveAnswers(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const obj = JSON.parse(data);
        if (obj.type == 'answer') {
            const answerList = document.querySelector("#answerList");
            const answer = document.createElement("li");
            answer.textContent = obj.answer;
            answerList.appendChild(answer);
        } else {
            console.log(obj);
        }
    });
}

function doSomething(websocket) {
    const answerButton = document.querySelector("#doSomethingButton");
    answerButton.addEventListener("click", () => {
        const event = {
            type: "idk",
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