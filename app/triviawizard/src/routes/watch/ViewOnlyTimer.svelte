<svelte:options accessors={true}/>

<script lang="ts">
    export let duration = 30;
    export let timeRemaining = duration;
    let running = false;
    let interval: NodeJS.Timer;

    export function start() {
        running = true;
        interval = setInterval(() => {
            timeRemaining--;
            if (timeRemaining <= 0) {
                stop();
            }
        }, 1000);
    }

    export function stop() {
        clearInterval(interval);
        running = false;
    }

    export function reset() {
        stop();
        timeRemaining = duration;
    }

    $: minutes = Math.floor(timeRemaining / 60);
    $: seconds = timeRemaining % 60;
</script>

<div class="timer">{minutes}:{seconds < 10 ? '0' : ''}{seconds}</div>

<style>
    .timer {
        font-size: 3em;
        margin-right: 0.2em;
    }
</style>