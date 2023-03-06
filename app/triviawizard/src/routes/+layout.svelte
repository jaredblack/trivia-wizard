<script lang="ts">
    import '@picocss/pico'
    import '../app.css'
</script>
<main class="container">
    <header>
        <h1>Trivia Wizard</h1>
    </header>
</main>

<slot/>

<style>
    h1 {
        font-size: 3rem;
        font-weight: 700;
        margin-top: 1rem;
    }
</style>