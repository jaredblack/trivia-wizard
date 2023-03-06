<script lang='ts'>
	import type { AnswerObject } from '../../types';
    import { getWebSocketServer } from '../../utils'
	import Answer from './Answer.svelte';

    let gameCode: string;
    let websocket: WebSocket;
    let connected = false;
    let answerList: AnswerObject[] = [];

    async function generateGameCode() {
        const res = await fetch("https://random-word-api.herokuapp.com/word?length=5");
        const jsonCook = await res.json();
        if (res.ok) {
            gameCode = jsonCook[0].toUpperCase();
        } else {
            alert("Error generating game code");
        }
    }

    function createGame() {
        gameCode = gameCode.trim().toLocaleUpperCase();
        if (gameCode.length < 5 || gameCode.length > 5) {
            alert("Game code must be 5 characters long");
            return;
        }
        const websocket = new WebSocket(getWebSocketServer());

        websocket.addEventListener("open", () => {
            const event = {
                type: "init",
                gameCode: gameCode,
                create: true,
            };
            websocket.send(JSON.stringify(event));
        });
        receiveMessages(websocket);
    }

    function receiveMessages(websocket: WebSocket) {
        websocket.addEventListener("message", ({data}) => {
            const obj = JSON.parse(data);
            if (obj.type == 'answer') {
                console.log(obj);
                answerList = [...answerList, obj];
            } else if (obj.type == 'success') {
                console.log(obj);
                connected = true;
            } else if (obj.type == 'newQuestion') {
            
            }
        });
    }
</script>

<main class="container">
    {#if !connected}
    <label for="gameCodeInput">Game code</label>
    <input type="text" id="gameCodeInput" bind:value={gameCode} placeholder="Enter game code or generate new code"/>
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
        <h3>Answers</h3>
        {#if answerList.length == 0}
        <p>No answers yet</p>
        {:else}
        {#each answerList as answer}
        <Answer answerText={answer.answer} teamName={answer.teamName} />
        {/each}
        {/if}
    </div>
    {/if}
</main>

<style>
    #gameCodeInput {
        text-transform: uppercase;
    }

    #gameCodeInput::placeholder {
        text-transform: none;
    }

    .right {
        text-align: right;
    }
</style>