<script lang="ts">
	import type { AnswerObject } from '../../types';
	import { getWebSocketServer } from '../../utils';
	import Answer from './Answer.svelte';

	let gameCode: string;
	let websocket: WebSocket;
	let connected = false;
	let answerList: AnswerObject[] = [];
	let questionIndex = 0;

	const updateTeamScore = (teamName: string, teamScore: number) => {
		const event = {
			type: 'updateScore',
			teamName: teamName,
			score: teamScore
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
		receiveMessages(websocket);
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
			}
		});
	}

    function nextQuestion() {
        const event = {
            type: "next",
        };
        websocket.send(JSON.stringify(event));
    }

    function prevQuestion() {
        const event = {
            type: "prev",
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
					<button class="circular-icon-button" disabled={questionIndex < 2} on:click={prevQuestion}
						><span class="material-symbols-outlined"> arrow_back </span></button
					>
					<button class="circular-icon-button" on:click={nextQuestion}
						><span class="material-symbols-outlined"> arrow_forward </span></button
					>
				</div>
			</div>
			<h3>Answers</h3>
			{#if answerList.length == 0}
				<p>No answers yet</p>
			{:else}
				{#each answerList as answer}
					<Answer answerText={answer.answer} teamName={answer.teamName} updateTeamScore={updateTeamScore}/>
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

	#questionHeader {
		display: flex;
		justify-content: space-between;
	}

    #forwBackButtons {
        display: flex;
        justify-content: space-between;
    }
</style>
