<script lang="ts">
    import { onMount } from 'svelte';
    import { getWebSocketServer } from '../../utils';
    enum States {
        NotConnected,
        AnswersNotAllowed,
        InputAnswer
    }

    let state = States.NotConnected;
    let gameCode = '';
    let teamName = '';
    let errorText = '';
    let submittedAnswer = false;
    let gameCodeInvalid = false;
    let teamNameInvalid = false;
    let answerText = '';
    let websocket: WebSocket;
    let questionIndex = 0;
    let triedToRejoin = false;

    onMount(async () => {
        const savedGameCode = localStorage.getItem('gameCode');
        const savedTeamName = localStorage.getItem('teamName');
        if (savedGameCode && savedTeamName) {
            triedToRejoin = true;
            gameCode = savedGameCode;
            teamName = savedTeamName;
            joinGame();
        }
    });

    function joinGame() {
        gameCode = gameCode.toLocaleUpperCase();
        teamName = teamName.trim();
        gameCodeInvalid = gameCode === '' || gameCode.length != 5 ? true : false;
        teamNameInvalid = teamName === '' ? true : false;
        if (gameCodeInvalid || teamNameInvalid) {
            return;
        }

        websocket = new WebSocket(getWebSocketServer());
        websocket.addEventListener('open', () => {
            const event = {
                type: 'init',
                gameCode: gameCode,
                teamName: teamName,
                initType: 'player'
            };
            websocket.send(JSON.stringify(event));
        });
        websocket.onclose = reconnect;
        receiveMessages(websocket);
    }

    function reconnect() {
        console.log('Lost connection, reconnecting...');
        setTimeout(joinGame, 1000);
    }

    function updateAcceptingAnswers(acceptingAnswers: boolean) {
        if (acceptingAnswers) {
            state = States.InputAnswer;
        } else {
            state = States.AnswersNotAllowed;
        }
    }

    function saveJoinGameInfo() {
        localStorage.setItem('gameCode', gameCode);
        localStorage.setItem('teamName', teamName);
    }

    function receiveMessages(websocket: WebSocket) {
        websocket.addEventListener('message', ({ data }) => {
            const obj = JSON.parse(data);
            console.log(obj);
            if (obj.type === 'success') {
                saveJoinGameInfo();
                questionIndex = obj.questionIndex;
                updateAcceptingAnswers(obj.acceptingAnswers);
            } else if (obj.type === 'answerReceived') {
                state = States.AnswersNotAllowed;
            } else if (obj.type === 'updatePlayerQuestionIndex') {
                state = States.InputAnswer;
                submittedAnswer = false;
                answerText = '';
                questionIndex = obj.questionIndex;
            } else if (obj.type === 'updateAcceptingAnswers') {
                updateAcceptingAnswers(obj.acceptingAnswers);
                // auto-submit when timer runs out
                if (!obj.acceptingAnswers && obj.timeRemaining === 0 && !submittedAnswer) {
                    submitAnswer();
                }
            } else if (obj.type === 'error') {
                if (triedToRejoin) {
                    errorText = `Tried to rejoin game with code ${gameCode}, but it does not exist anymore.`;
                    gameCode = '';
                    teamName = '';
                } else {
                    errorText = obj.message;
                }
                websocket.onclose = null;
            }
        });
    }

    function submitAnswer() {
        submittedAnswer = true;
        const event = {
            type: 'answer',
            answer: answerText,
            teamName: teamName,
            questionIndex: questionIndex
        };
        websocket.send(JSON.stringify(event));
    }

    function gameCodeExists(savedGameCode: string) {}
</script>

<main class="container">
    {#if state === States.NotConnected}
        <label for="gameCodeInput">Game code</label>
        <input
            type="text"
            id="gameCodeInput"
            bind:value={gameCode}
            placeholder="Enter game code"
            aria-invalid={gameCodeInvalid || null}
        />
        <label for="teamNameInput">Team name</label>
        <input
            type="text"
            id="teamNameInput"
            bind:value={teamName}
            placeholder="Enter team name"
            aria-invalid={teamNameInvalid || null}
        />
        <p class="error">{errorText}</p>
        <button on:click={joinGame}>Join Game</button>
    {:else}
        <div class="nameCodeBar">
            <h5 id="teamNameView">{teamName}</h5>
            <h5>Game code: {gameCode}</h5>
        </div>
        {#if state === States.InputAnswer}
            <h1>Question {questionIndex}</h1>
            <textarea bind:value={answerText} name="Answer" id="answerText" cols="30" rows="10" />
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
