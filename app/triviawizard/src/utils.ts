export function getWebSocketServer() {
    if (window.location.host ==="jaredblack.github.io") {
        return "wss://triviawizard.herokuapp.com";
    } else {
        return "ws://localhost:8001";
    }
}