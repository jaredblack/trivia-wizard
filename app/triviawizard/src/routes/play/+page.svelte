<script lang="ts">
	import { getWebSocketServer } from "../../utils";
    enum States {
        NotConnected,
        AnswersNotAllowed,
        InputAnswer
    }

    let state = States.NotConnected;
    let gameCode = "";
    let teamName = "";
    let errorText = "";
    let connected = false;
    let gameCodeInvalid = false;
    let teamNameInvalid = false;
    let answerText = "";
    let websocket: WebSocket;
    let questionIndex = 0;
    
    function joinGame() {
        if (gameCode === "" || gameCode.length != 5) {
            gameCodeInvalid = true;
        } else {
            gameCodeInvalid = false;
        }
        if (teamName === "") {
            teamNameInvalid = true;
        } else {
            teamNameInvalid = false;
        }

        websocket = new WebSocket(getWebSocketServer());
        websocket.addEventListener("open", () => {
            const event = {
                type: "init",
                gameCode: gameCode,
                teamName: teamName,
                initType: "player"
            };
            websocket.send(JSON.stringify(event));
        });
        receiveMessages(websocket);
    }

    function updateAcceptingAnswers(acceptingAnswers: boolean) {
        if (acceptingAnswers) {
            state = States.InputAnswer;
        } else {
            state = States.AnswersNotAllowed;
        }
    }

	function receiveMessages(websocket: WebSocket) {
        websocket.addEventListener("message", ({data}) => {
            const obj = JSON.parse(data);
            console.log(obj);
            if (obj.type === "success") {
                // TODO: this really should update to a correct state based on if we've submitted an answer for that question yet
                questionIndex = obj.questionIndex;
                updateAcceptingAnswers(obj.acceptingAnswers);
            } else if (obj.type === "answerReceived") {
                state = States.AnswersNotAllowed;
            } else if (obj.type === "updatePlayerQuestionIndex") {
                state = States.InputAnswer;
                answerText = "";
                questionIndex = obj.questionIndex;
            } else if (obj.type === "updateAcceptingAnswers") {
                updateAcceptingAnswers(obj.acceptingAnswers);
            }
        });
	}

    function submitAnswer() {
        const event = {
            type: "answer",
            answer: answerText,
            teamName: teamName,
            questionIndex: questionIndex,
        };
        websocket.send(JSON.stringify(event));
    }


</script>

<main class="container">
    {#if state === States.NotConnected}
        <label for="gameCodeInput">Game code</label>
        <input type="text" id="gameCodeInput" bind:value={gameCode} placeholder="Enter game code" aria-invalid={gameCodeInvalid || null}/>
        <label for="teamNameInput">Team name</label>
        <input type="text" id="gameCodeInput" bind:value={teamName} placeholder="Enter team name" aria-invalid={teamNameInvalid || null}/>
        <p class="error">{errorText}</p>
        <button on:click={joinGame}>Join Game</button>
    {:else}
        <div class="nameCodeBar">
            <h5 id="teamNameView">{teamName}</h5>
            <h5>Game code: {gameCode}</h5>
        </div>
        {#if state === States.InputAnswer}
            <h1>Question {questionIndex}</h1>
            <textarea bind:value={answerText} name="Answer" id="answerText" cols="30" rows="10"></textarea>
            <button on:click={submitAnswer}>Submit Answer</button>
        {:else if state === States.AnswersNotAllowed}
            <p>Answers not allowed yet...or maybe we're just waiting for the next question</p>
        {/if}
    {/if}
</main>

<style>
    .error {
        color: rgb(198, 107, 107);
        font-style: italic;
    }

    .nameCodeBar {
        display: flex;
        justify-content: space-between;
    }

    #teamNameView {
        font-style: italic;
    }
</style>