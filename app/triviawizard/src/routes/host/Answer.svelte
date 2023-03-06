<div class="answer-container">
    <div class="answer-view">
        <h5>{teamName}</h5>
        <p>{answerText}</p>
    </div>
    <div class="score-controls">
        <button class="increment-button secondary"><span class="material-symbols-outlined">
            close
            </span></button>
        <h2 class="score-display">{teamScore}</h2>
        <button class="increment-button secondary"><span class="material-symbols-outlined">
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

    .increment-button {
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        margin: 0;
        width: 50px;
        height: 50px;
        padding: 0;
        border: none;
    }

    .material-symbols-outlined {
        display: inline-block;
        width: 24px;
        height: 24px;
        font-size: 24px;
        text-align: center;
    }

    h5 {
        margin: 0;
    }

    p {
        margin: 0;
    }

    .material-symbols-outlined {
        font-variation-settings:
        'FILL' 0,
        'wght' 400,
        'GRAD' 0,
        'opsz' 48
    }

</style>