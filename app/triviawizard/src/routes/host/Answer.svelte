<div class="answer-container">
    <div class="answer-view">
        <h5>{teamName}</h5>
        <p>{answerText}</p>
    </div>
    <div class="score-controls">
        <button class="circular-icon-button secondary"><span class="material-symbols-outlined">
            close
            </span></button>
        <h2 class="score-display">{teamScore}</h2>
        <button class="circular-icon-button secondary"><span class="material-symbols-outlined">
            done
            </span></button>
    </div>
</div>

<script>
    export let teamName = "Team 1";
    export let answerText = "This is the answer text";
    export let teamScore = 0;
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