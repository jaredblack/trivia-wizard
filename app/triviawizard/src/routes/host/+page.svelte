<script lang="ts">
    import type { AnswerObject } from '../../types';
    import { getWebSocketServer } from '../../utils';
    import Answer from './Answer.svelte';
    import Timer from './Timer.svelte';

    let gameCode: string;
    let websocket: WebSocket;
    let connected = false;
    let answerList: AnswerObject[] = [];
    let questionIndex = 0;
    let timerElement: Timer;
    let timerDuration: number = 30;
    let questionPoints: number = 50;
    let multiScoring: boolean = false;

    const updateTeamScore = (teamName: string, teamScore: number, pointsGiven: number) => {
        const event = {
            type: 'updateScore',
            teamName: teamName,
            score: teamScore,
            pointsGiven: pointsGiven
        };
        websocket.send(JSON.stringify(event));
    };

    const updateAcceptingAnswers = (acceptingAnswers: boolean) => {
        const event = {
            type: 'updateAcceptingAnswers',
            acceptingAnswers: acceptingAnswers,
            questionIndex: questionIndex,
            timeRemaining: timerElement.timeRemaining
        };
        websocket.send(JSON.stringify(event));
    };

    async function generateGameCode() {
        const res = await fetch('https://random-word-api.herokuapp.com/word?length=5');
        const jsonCook = await res.json();
        if (res.ok) {
            gameCode = jsonCook[0].toUpperCase();
        } else {
            alert('Error generating game code');
        }
    }

    function createGame() {
        gameCode = gameCode.trim().toLocaleUpperCase();
        if (gameCode.length < 5 || gameCode.length > 5) {
            alert('Game code must be 5 characters long');
            return;
        }
        websocket = new WebSocket(getWebSocketServer());

        websocket.addEventListener('open', () => {
            const event = {
                type: 'init',
                gameCode: gameCode,
                initType: 'host'
            };
            websocket.send(JSON.stringify(event));
        });

        websocket.onclose = reconnect;
        receiveMessages(websocket);
    }

    function reconnect() {
        console.log('Lost connection, reconnecting...');
        setTimeout(createGame, 1000);
    }

    function receiveMessages(websocket: WebSocket) {
        websocket.addEventListener('message', ({ data }) => {
            const obj = JSON.parse(data);
            if (obj.type == 'answer') {
                console.log(obj);
                answerList = [...answerList, obj];
            } else if (obj.type == 'success') {
                console.log(obj);
                connected = true;
                questionIndex = obj.questionIndex;
            } else if (obj.type == 'newQuestion') {
                answerList = obj.answers;
                questionIndex = obj.questionIndex;
                timerElement.reset();
                // TODO: these two should be kept track of on a per-question basis so we can see how many points things were worth/how much time looking back
                // I don't think this will be a huge problem though and it would require creating a notion of a Question in the db which we don't have currently
                timerDuration = 30;
                questionPoints = 50;
                multiScoring = false;
            }
        });
    }

    function nextQuestion() {
        const event = {
            type: 'next'
        };
        websocket.send(JSON.stringify(event));
    }

    function prevQuestion() {
        const event = {
            type: 'prev'
        };
        websocket.send(JSON.stringify(event));
    }
</script>

<main class="container">
    {#if !connected}
        <label for="gameCodeInput">Game code</label>
        <input
            type="text"
            id="gameCodeInput"
            bind:value={gameCode}
            placeholder="Enter game code or generate new code"
        />
        <div class="grid">
            <div>
                <button on:click={generateGameCode}>Generate game code</button>
            </div>
            <div>
                <button on:click={createGame}>Create game</button>
            </div>
        </div>
    {:else}
        <div>
            <h3 class="right">Game code: {gameCode}</h3>
            <div id="questionHeader">
                <h1>Question {questionIndex}</h1>
                <div id="forwBackButtons">
                    <button
                        class="circular-icon-button"
                        disabled={questionIndex < 2}
                        on:click={prevQuestion}
                        ><span class="material-symbols-outlined"> arrow_back </span></button
                    >
                    <button class="circular-icon-button" on:click={nextQuestion}
                        ><span class="material-symbols-outlined"> arrow_forward </span></button
                    >
                </div>
            </div>
            <Timer
                bind:duration={timerDuration}
                {updateAcceptingAnswers}
                bind:this={timerElement}
            />
            <h3>Answers</h3>
            {#if answerList.length == 0}
                <p>No answers yet</p>
            {:else}
                {#each answerList as answer}
                    <Answer
                        answerText={answer.answer}
                        teamName={answer.teamName}
                        {updateTeamScore}
                        teamScore={answer.teamScore}
                        pointsGiven={answer.pointsGiven}
                        {questionPoints}
                        bind:multiScoring
                    />
                {/each}
            {/if}
        </div>
        <div class="footer">
            <label for="timerDuration"
                >Timer duration
                <input
                    type="number"
                    id="timerDuration"
                    bind:value={timerDuration}
                    placeholder="countdown"
                    class="smallNumInput"
                />
            </label>
            <label for="questionPoints" class="numberInputLabel"
                >Question points
                <input
                    type="number"
                    id="questionPoints"
                    bind:value={questionPoints}
                    class="smallNumInput"
                />
            </label>
            <fieldset>
                <label for="multiScoreSwitch"
                    >Multi-scoring
                    <input
                        type="checkbox"
                        role="switch"
                        id="multiScoreSwitch"
                        bind:checked={multiScoring}
                    />
                </label>
            </fieldset>
        </div>
    {/if}
</main>

<style>
    .right {
        text-align: right;
    }

    #questionHeader {
        display: flex;
        justify-content: space-between;
    }

    #forwBackButtons {
        display: flex;
        justify-content: space-between;
    }

    .footer {
        justify-content: space-between;
        align-items: center;
        display: flex;
        width: 100%;
        box-sizing: border-box;
    }

    .numberInputLabel {
        margin: 0;
    }

    .smallNumInput {
        width: 100px;
    }
</style>
