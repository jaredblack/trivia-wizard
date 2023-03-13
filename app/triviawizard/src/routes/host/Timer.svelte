<svelte:options accessors={true}/>

<script lang="ts">
    export let duration = 30;
    export let updateAcceptingAnswers = (shouldAccept: boolean) => {};
    export let timeRemaining = duration;
    let running = false;
    let interval: NodeJS.Timer;

    function start() {
        running = true;
        updateAcceptingAnswers(true);
        interval = setInterval(() => {
            timeRemaining--;
            if (timeRemaining <= 0) {
                stop();
            }
        }, 1000);
    }

    function stop() {
        clearInterval(interval);
        updateAcceptingAnswers(false);
        running = false;
    }

    export function reset() {
        stop();
        timeRemaining = duration;
    }

    $: timeRemaining = duration
    $: minutes = Math.floor(timeRemaining / 60);
    $: seconds = timeRemaining % 60;
</script>


<div class="timer-container">
    {#if running}
      <div class="timer">{minutes}:{seconds < 10 ? '0' : ''}{seconds}</div>
      <button class="circular-icon-button" on:click={stop}><span class="material-symbols-outlined">
        pause
        </span></button>
    {:else}
      <div class="timer">{minutes}:{seconds < 10 ? '0' : ''}{seconds}</div>
      <button class="circular-icon-button" on:click={start}><span class="material-symbols-outlined">
        play_arrow
        </span></button>
    {/if}
    <button class="circular-icon-button" on:click={reset}><span class="material-symbols-outlined">
        restart_alt
        </span></button>
</div>


<style>
    .timer {
        font-size: 3em;
        margin-right: 0.2em;
    }
    .timer-container {
        display: flex;
        flex-direction: row;
        justify-content: end;
        align-items: center;
    }
</style>