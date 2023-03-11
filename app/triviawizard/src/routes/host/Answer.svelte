<div class="answer-container">
    <div class="answer-view">
        <h5>{teamName}</h5>
        <p>{answerText}</p>
    </div>
    <div class="score-controls">
        <button class="circular-icon-button secondary" style="background-color: {incorrectButtonColor}" on:click={markQuestionIncorrect}><span class="material-symbols-outlined">
            close
            </span></button>
        <h2 class="score-display">{teamScore}</h2>
        <button class="circular-icon-button secondary" style="background-color: {correctButtonColor}" on:click={markQuestionCorrect}><span class="material-symbols-outlined">
            done
            </span></button>
    </div>
</div>

<script lang="ts">
	import { onMount } from "svelte";


    export let teamName = "Team 1";
    export let answerText = "This is the answer text";
    export let teamScore = 0;
    export let updateTeamScore = (teamName: string, teamScore: number, pointsGiven: number) => {};
    export let pointsGiven = -1;
    let pointsAdded = false;

    $: correctButtonColor = pointsGiven > 0 ? 'var(--ins-color, green)' : 'var(--secondary, gray)';	
    $: incorrectButtonColor = pointsGiven == 0 ? 'var(--del-color, red)' : 'var(--secondary, gray)';

    onMount(() => {
        if (pointsGiven > 0) {
            pointsAdded = true;
        }
    });

    function markQuestionCorrect() {
        pointsGiven = 50;
        if (!pointsAdded) {
            teamScore += pointsGiven;
            updateTeamScore(teamName, teamScore, pointsGiven);
        }
        pointsAdded = true;
    }

    function markQuestionIncorrect() {
        pointsGiven = 0;
        if (pointsAdded) {
            teamScore -= 50;
            pointsAdded = false;
            updateTeamScore(teamName, teamScore, 0);
        }
    }
</script>

<style>
    .answer-container {
        border: 1px solid var(--primary, white);
        /* background-color: var(--secondary, white); */
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .score-controls {
        /* flex-grow: 3; */
        flex-basis: 0;
        display: flex;
        justify-content: center;
    }

    .score-display {
        text-align: center;
        margin: 0 10px 0 10px;
        padding: 0;
    }

    h5 {
        margin: 0;
    }

    p {
        margin: 0;
    }



</style>