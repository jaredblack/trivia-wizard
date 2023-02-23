"use strict";
window.addEventListener("DOMContentLoaded", () => {
    const questionIndex = document.querySelector("#questionIndex");
    questionIndex.textContent = 1;
});

function submitJoin() {
    const websocket = new WebSocket(getWebSocketServer());

    websocket.addEventListener("open", () => {
        const gameCode = document.querySelector("#joinInput").value;
        const teamName = document.querySelector("#teamNameInput").value;
        const event = {
            type: "init",
            gameCode: gameCode,
            teamName: teamName,
        }
        console.log("sending event: " + JSON.stringify(event));
        websocket.send(JSON.stringify(event));
    });
    submitAnswer(websocket);
    receiveMessages(websocket);
}

function submitAnswer(websocket) {
    const answerButton = document.querySelector("#answerButton");
    answerButton.addEventListener("click", () => {
        const questionIndex = document.querySelector("#questionIndex").textContent;
        const answer = document.querySelector("#answerInput").value;
        const teamName = document.querySelector("#teamNameInput").value;
        const event = {
            type: "answer",
            teamName: teamName,
            answer: answer,
            questionIndex: questionIndex,
        }
        websocket.send(JSON.stringify(event));
    });
}

function receiveMessages(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const obj = JSON.parse(data);
        if (obj.type == 'updateQuestionIndex') {
            const questionIndex = document.querySelector("#questionIndex");
            questionIndex.textContent = obj.questionIndex;
        }
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
