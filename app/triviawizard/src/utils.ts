export function getWebSocketServer() {
    if (window.location.host ==="jaredblack.github.io" || window.location.host === "trivia-wizard.vercel.app") {
        return "wss://triviawizard.herokuapp.com";
    } else {
        return "ws://localhost:8001";
    }
}