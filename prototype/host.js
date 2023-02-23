"use strict";
window.addEventListener("DOMContentLoaded", () => {
    const questionIndex = document.querySelector("#questionIndex");
    questionIndex.textContent = 1;
});

function submitCreate() {
    const gameCode = document.querySelector('#textCreateJoin').value;
    console.log(gameCode);
    const websocket = new WebSocket(getWebSocketServer());
    // initSocket(websocket, gameCode);
    websocket.addEventListener("open", () => {
        const event = {
            type: "init",
            gameCode: gameCode,
            create: true,
        };
        websocket.send(JSON.stringify(event));
    });
    receiveAnswers(websocket);
    nextQuestion(websocket);
    prevQuestion(websocket);
}

function receiveAnswers(websocket) {
    websocket.addEventListener("message", ({data}) => {
        const obj = JSON.parse(data);
        if (obj.type == 'answer') {
            const answerList = document.querySelector("#answerList");
            const answer = document.createElement("li");
            answer.textContent = `${obj.teamName}: ${obj.answer}`;
            answerList.appendChild(answer);
        } else if (obj.type == 'success') {
            console.log(obj);
            const connDisplay = document.querySelector("#connectionDisplay");
            connDisplay.textContent = `Connected to ${obj.gameCode}`
        } else if (obj.type == 'newQuestion') {
            const questionIndex = document.querySelector("#questionIndex");
            questionIndex.textContent = obj.questionIndex;
            const answerList = document.querySelector("#answerList");
            answerList.innerHTML = "";
            for (let answer of obj.answers) {
                const answerElement = document.createElement("li");
                answerElement.textContent = `${answer.teamName}: ${answer.answer}`;
                answerList.appendChild(answerElement);
            }
        }
    });
}

function nextQuestion(websocket) {
    const nextButton = document.querySelector("#nextButton");
    nextButton.addEventListener("click", () => {
        const event = {
            type: "next",
        };
        websocket.send(JSON.stringify(event));
    });
}

function prevQuestion(websocket) {
    const prevButton = document.querySelector("#prevButton");
    prevButton.addEventListener("click", () => {
        const event = {
            type: "prev",
        };
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