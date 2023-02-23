<script lang='ts'>
    import { getWebSocketServer } from '../../utils'

    let gameCode: string;
    let websocket: WebSocket;

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
        receiveAnswers(websocket);
    }

    function receiveAnswers(websocket: WebSocket) {
        websocket.addEventListener("message", ({data}) => {
            const obj = JSON.parse(data);
            if (obj.type == 'answer') {
                console.log(obj);
            } else if (obj.type == 'success') {
                console.log(obj);
            
            } else if (obj.type == 'newQuestion') {
            
            }
        });
    }
</script>

<main class="container">
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
</main>

<style>
    #gameCodeInput {
        text-transform: uppercase;
    }

    #gameCodeInput::placeholder {
        text-transform: none;
    }
</style>