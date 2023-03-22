<script lang="ts">
    import { onMount } from 'svelte';

    export let teamName = 'Team 1';
    export let answerText = 'This is the answer text';
    export let teamScore = 0;
    export let updateTeamScore = (teamName: string, teamScore: number, pointsGiven: number) => {};
    export let pointsGiven = -1;
    export let questionPoints = 50;
    export let multiScoring = false;
    export let bonusWeight = 0;
    let pointsAdded = false;
    let numberOfAnswersCorrect: number;
    let firstMount = true;
    const BONUS_AMOUNT = 5;

    $: numberOfAnswersCorrect = Math.floor(pointsGiven / questionPoints);

    $: correctButtonColor = pointsGiven > 0 ? 'var(--ins-color, green)' : 'var(--secondary, gray)';
    $: incorrectButtonColor = pointsGiven == 0 ? 'var(--del-color, red)' : 'var(--secondary, gray)';
    // switching between multiScoring and not will destroy previously scored point values so b careful
    $: toggleMultiScoring(multiScoring);
    $: recalculatePointsGiven(bonusWeight)

    function recalculatePointsGiven(bonusWeight: number) {
        if (pointsGiven > 0 && !multiScoring) {
            pointsGiven = (numberOfAnswersCorrect * questionPoints) + (bonusWeight * BONUS_AMOUNT);
        }
    }

    function toggleMultiScoring(multiScoring: boolean) {
        if (firstMount) {
            firstMount = false;
            return;
        }
        console.log("multiScoring: " + multiScoring);
        if (multiScoring) {
            pointsGiven = 0;
            if (pointsAdded) {
                teamScore -= questionPoints;
                pointsAdded = false;
                updateTeamScore(teamName, teamScore, pointsGiven);
            }
        } else if (pointsGiven > 0) {
            console.log("taking away points because we disabled multiscoring");
            teamScore -= pointsGiven;
            pointsGiven = 0;
            updateTeamScore(teamName, teamScore, pointsGiven);
            pointsAdded = false;
        }
    }

    onMount(() => {
        if (pointsGiven > 0) {
            pointsAdded = true;
        }
    });

    function markQuestionCorrect() {
        pointsGiven = questionPoints;
        if (!pointsAdded) {
            teamScore += pointsGiven;
            console.log("teamScore: " + teamScore);
            updateTeamScore(teamName, teamScore, pointsGiven);
            console.log("teamScore: " + teamScore + " pointsGiven: " + pointsGiven);
        }
        pointsAdded = true;
    }

    function markQuestionIncorrect() {
        pointsGiven = 0;
        if (pointsAdded) {
            teamScore -= questionPoints;
            pointsAdded = false;
            updateTeamScore(teamName, teamScore, 0);
        }
    }

    function addMultiScorePoints() {
        pointsGiven += questionPoints;
        teamScore += questionPoints;
        updateTeamScore(teamName, teamScore, pointsGiven);
    }

    function removeMultiScorePoints() {
        pointsGiven -= questionPoints;
        teamScore -= questionPoints;
        updateTeamScore(teamName, teamScore, pointsGiven);
    }
</script>

<div class="answer-container">
    <div class="answer-view">
        <h5>{teamName}</h5>
        <p>{answerText}</p>
    </div>
    <div class="score-controls">
        {#if !multiScoring}
            <button
                class="circular-icon-button secondary"
                style="background-color: {incorrectButtonColor}"
                on:click={markQuestionIncorrect}
                ><span class="material-symbols-outlined"> close </span></button
            >
            <h2 class="score-display">{teamScore}</h2>
            <button
                class="circular-icon-button secondary"
                style="background-color: {correctButtonColor}"
                on:click={markQuestionCorrect}
                ><span class="material-symbols-outlined"> done </span></button
            >
        {:else}
            <span class="numMarkedDisplay">{numberOfAnswersCorrect} × {questionPoints}</span>
            <button class="circular-icon-button secondary" on:click={removeMultiScorePoints}
                ><span class="material-symbols-outlined"> remove </span></button
            >
            <h2 class="score-display">{teamScore}</h2>
            <button class="circular-icon-button secondary" on:click={addMultiScorePoints}
                ><span class="material-symbols-outlined"> add </span></button
            >
        {/if}
    </div>
</div>

<style>
    .answer-container {
        border: 1px solid var(--primary, white);
        padding: 10px;
        margin: 10px;
        border-radius: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .score-controls {
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

    .numMarkedDisplay {
        margin: 0 10px 0 10px;
        padding: 0;
        margin-top: auto;
        color: var(--muted-color, gray);
    }
</style>
