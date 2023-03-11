<script lang="ts">
	import type { TeamScore } from "../../types";
	import { getWebSocketServer } from "../../utils";

    let teamScores: TeamScore[] = [];
    let gameCode: string;
    let websocket: WebSocket;
    let connected = false;


    function watchGame() {
        websocket = new WebSocket(getWebSocketServer());
        websocket.addEventListener('open', () => {
            const event = {
                type: 'init',
                gameCode: gameCode,
                initType: 'watch'
            };
            connected = true;
            websocket.send(JSON.stringify(event));
        });
        websocket.addEventListener('message', ({ data }) => {
            const obj = JSON.parse(data);
            console.log(obj);
            if (obj.type == 'teamScores') {
                teamScores = obj.teamScores;
            }
        });
    }
    
</script>

<div>
    <div class="container">
        {#if !connected}
            <label for="gameCodeInput">Game code</label>
            <input
                type="text"
                id="gameCodeInput"
                bind:value={gameCode}
                placeholder="Enter game code or generate new code"
            />
            <button on:click={watchGame}>Watch game</button>
        {:else}
        <h4 class="right-justify">Game code: {gameCode}</h4>
        <h1>Teams:</h1>
        <ol>
        {#each teamScores as team}
            <li>{team.teamName}: {team.score}</li>
        {/each}
        </ol>
        {/if}
    </div>
</div>